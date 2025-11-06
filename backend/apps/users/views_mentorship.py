"""
Views for mentorship matching system
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Q

from .models_mentorship import SuccessStory, ProfileMatch, MentorshipRequest
from .serializers_mentorship import (
    SuccessStorySerializer,
    ProfileMatchSerializer,
    MentorshipRequestSerializer,
    SendMentorshipRequestSerializer,
    RespondMentorshipRequestSerializer,
)

User = get_user_model()


def calculate_profile_similarity(user1, user2):
    """
    Calculate similarity between two user profiles
    Returns score 0-100
    """
    score = 0
    
    # Get user skills
    user1_skills = set([s.lower() for s in (user1.skills or [])])
    user2_skills = set([s.lower() for s in (user2.skills or [])])
    
    # Skills overlap (60% weight - aumentado para dar más importancia)
    if user1_skills and user2_skills:
        intersection = user1_skills.intersection(user2_skills)
        union = user1_skills.union(user2_skills)
        skill_similarity = (len(intersection) / len(union)) * 100 if union else 0
        score += skill_similarity * 0.6
    
    # Location match (20% weight)
    if user1.location and user2.location:
        if user1.location.lower() == user2.location.lower():
            score += 20
    
    # Experience level similarity (20% weight - reducido)
    # Compare based on experience field
    if user1.experience and user2.experience:
        exp1 = user1.experience.lower()
        exp2 = user2.experience.lower()
        
        # Simple experience level matching
        levels = {
            'junior': 1,
            'mid': 2,
            'senior': 3,
            'lead': 4,
        }
        
        level1 = next((v for k, v in levels.items() if k in exp1), 0)
        level2 = next((v for k, v in levels.items() if k in exp2), 0)
        
        if level1 and level2:
            diff = abs(level1 - level2)
            if diff == 0:
                score += 20
            elif diff == 1:
                score += 15
            elif diff == 2:
                score += 10
                score += 10
    
    return min(100, round(score))


class MentorshipViewSet(viewsets.GenericViewSet):
    """ViewSet for mentorship matching and connections"""
    
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def find_mentors(self, request):
        """
        Find potential mentors based on profile similarity
        GET /api/auth/mentorship/find_mentors/
        """
        user = request.user
        
        # Get all users with success stories who are willing to mentor
        mentors = User.objects.filter(
            success_story__is_willing_to_mentor=True,
            success_story__is_active=True
        ).exclude(id=user.id)
        
        # Calculate or get cached matches
        matches = []
        for mentor in mentors:
            # Check if match already calculated
            match, created = ProfileMatch.objects.get_or_create(
                user=user,
                matched_user=mentor,
                defaults={'similarity_score': 0}
            )
            
            # Recalculate if old (more than 7 days) or just created
            if created or (timezone.now() - match.calculated_at).days > 7:
                score = calculate_profile_similarity(user, mentor)
                
                # Calculate matching details
                user_skills = set([s.lower() for s in (user.skills or [])])
                mentor_skills = set([s.lower() for s in (mentor.skills or [])])
                matching_skills = list(user_skills.intersection(mentor_skills))
                
                skill_overlap = 0
                if user_skills:
                    skill_overlap = (len(matching_skills) / len(user_skills)) * 100
                
                match.similarity_score = score
                match.matching_skills = matching_skills
                match.skill_overlap_percentage = round(skill_overlap, 2)
                match.same_location = (
                    user.location and mentor.location and
                    user.location.lower() == mentor.location.lower()
                )
                match.save()
            
            matches.append(match)
        
        # Filter matches with score >= 5 (cambiado de 30 para mostrar más resultados)
        matches = [m for m in matches if m.similarity_score >= 5]
        matches.sort(key=lambda x: x.similarity_score, reverse=True)
        
        # Limit to top 20 matches
        matches = matches[:20]
        
        serializer = ProfileMatchSerializer(matches, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def send_request(self, request):
        """
        Send mentorship request to a mentor
        POST /api/auth/mentorship/send_request/
        Body: {"to_user_id": "uuid-string", "message": "..."}
        """
        serializer = SendMentorshipRequestSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        
        mentorship_request = MentorshipRequest.objects.create(
            from_user=request.user,
            to_user_id=serializer.validated_data['to_user_id'],
            message=serializer.validated_data['message']
        )
        
        response_serializer = MentorshipRequestSerializer(mentorship_request)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def my_requests(self, request):
        """
        Get user's sent and received mentorship requests
        GET /api/auth/mentorship/my_requests/?type=sent|received
        """
        request_type = request.query_params.get('type', 'all')
        
        if request_type == 'sent':
            requests = MentorshipRequest.objects.filter(
                from_user=request.user
            )
        elif request_type == 'received':
            requests = MentorshipRequest.objects.filter(
                to_user=request.user
            )
        else:
            # All requests (both sent and received)
            requests = MentorshipRequest.objects.filter(
                Q(from_user=request.user) | Q(to_user=request.user)
            )
        
        serializer = MentorshipRequestSerializer(requests, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def respond(self, request, pk=None):
        """
        Respond to a mentorship request (accept or decline)
        POST /api/auth/mentorship/{id}/respond/
        Body: {"action": "accept"|"decline", "response_message": "..."}
        """
        try:
            mentorship_request = MentorshipRequest.objects.get(
                id=pk,
                to_user=request.user,
                status='pending'
            )
        except MentorshipRequest.DoesNotExist:
            return Response(
                {'error': 'Solicitud no encontrada o no autorizada'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = RespondMentorshipRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        action_type = serializer.validated_data['action']
        response_message = serializer.validated_data.get('response_message', '')
        
        if action_type == 'accept':
            # Check if mentor can still accept mentees
            if not request.user.success_story.can_accept_mentees:
                return Response(
                    {'error': 'Has alcanzado el límite de mentorados'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            mentorship_request.status = 'accepted'
        else:
            mentorship_request.status = 'declined'
        
        mentorship_request.response_message = response_message
        mentorship_request.responded_at = timezone.now()
        mentorship_request.save()
        
        response_serializer = MentorshipRequestSerializer(mentorship_request)
        return Response(response_serializer.data)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        Cancel a sent mentorship request
        POST /api/auth/mentorship/{id}/cancel/
        """
        try:
            mentorship_request = MentorshipRequest.objects.get(
                id=pk,
                from_user=request.user,
                status='pending'
            )
        except MentorshipRequest.DoesNotExist:
            return Response(
                {'error': 'Solicitud no encontrada o no puede ser cancelada'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        mentorship_request.status = 'cancelled'
        mentorship_request.save()
        
        serializer = MentorshipRequestSerializer(mentorship_request)
        return Response(serializer.data)


__all__ = ['MentorshipViewSet']

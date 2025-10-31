# 🤖 Chatbot con IA para Joby

## Descripción

El chatbot de Joby utilizará inteligencia artificial para proporcionar recomendaciones personalizadas de trabajos basándose en el perfil del usuario, sus habilidades, experiencia y preferencias.

## Características del Chatbot

### 1. Análisis de Perfil
- Analiza automáticamente el perfil del usuario
- Identifica habilidades clave
- Evalúa experiencia y educación
- Detecta preferencias de ubicación y tipo de trabajo

### 2. Recomendaciones Personalizadas
- Sugiere trabajos compatibles con el perfil
- Explica por qué un trabajo es adecuado
- Calcula porcentaje de compatibilidad
- Prioriza trabajos según preferencias

### 3. Conversación Natural
- Responde preguntas sobre trabajos
- Ayuda a mejorar el perfil
- Da consejos para aplicaciones
- Prepara al usuario para entrevistas

### 4. Asistencia en Tiempo Real
- Disponible 24/7
- Respuestas instantáneas
- Contexto de conversación mantenido
- Historial de chat guardado

## Arquitectura Técnica

### Opción 1: OpenAI GPT-4
```python
# Backend Django - chatbot/views.py
import openai
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

openai.api_key = settings.OPENAI_API_KEY

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat_message(request):
    user = request.user
    message = request.data.get('message')
    
    # Construir contexto del usuario
    user_context = f"""
    Perfil del Usuario:
    - Nombre: {user.name}
    - Habilidades: {', '.join(user.skills)}
    - Experiencia: {user.experience}
    - Educación: {user.education}
    - Ubicación: {user.location}
    """
    
    # Obtener trabajos disponibles
    jobs = Job.objects.filter(status='Open')[:10]
    jobs_context = "\n".join([
        f"- {job.title} en {job.company} ({job.location}): {job.requirements}"
        for job in jobs
    ])
    
    # Crear prompt
    system_prompt = f"""
    Eres un asistente de búsqueda de empleo especializado. 
    Ayuda a los usuarios a encontrar trabajos adecuados basándote en su perfil.
    
    {user_context}
    
    Trabajos Disponibles:
    {jobs_context}
    """
    
    # Llamar a OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ],
        temperature=0.7,
        max_tokens=500
    )
    
    ai_message = response.choices[0].message.content
    
    # Guardar en base de datos
    ChatMessage.objects.create(
        user=user,
        message=message,
        response=ai_message,
        context={'jobs_analyzed': len(jobs)}
    )
    
    return Response({
        'message': ai_message,
        'timestamp': datetime.now()
    })
```

### Opción 2: Google Gemini
```python
import google.generativeai as genai

genai.configure(api_key=settings.GOOGLE_API_KEY)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat_message_gemini(request):
    user = request.user
    message = request.data.get('message')
    
    # Configurar modelo
    model = genai.GenerativeModel('gemini-pro')
    
    # Construir prompt similar al anterior
    prompt = f"""
    Como asistente de búsqueda de empleo, ayuda al usuario.
    
    Perfil: {user.name}, habilidades: {user.skills}
    Pregunta: {message}
    """
    
    response = model.generate_content(prompt)
    
    return Response({
        'message': response.text,
        'timestamp': datetime.now()
    })
```

## Implementación en Flutter

### 1. Modelo de Chat
```dart
// lib/models/chat_message.dart
class ChatMessage {
  final String id;
  final String message;
  final bool isUser;
  final DateTime timestamp;
  
  ChatMessage({
    required this.id,
    required this.message,
    required this.isUser,
    required this.timestamp,
  });
}
```

### 2. Servicio de Chatbot
```dart
// lib/services/chatbot_service.dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class ChatbotService {
  final String baseUrl = 'http://localhost:8000/api/chatbot';
  
  Future<String> sendMessage(String message, String token) async {
    final response = await http.post(
      Uri.parse('$baseUrl/message/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: jsonEncode({'message': message}),
    );
    
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return data['message'];
    } else {
      throw Exception('Error al enviar mensaje');
    }
  }
  
  Future<List<Map<String, dynamic>>> getRecommendations(String token) async {
    final response = await http.post(
      Uri.parse('$baseUrl/recommend/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
    );
    
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return List<Map<String, dynamic>>.from(data['recommendations']);
    } else {
      throw Exception('Error al obtener recomendaciones');
    }
  }
}
```

### 3. Pantalla de Chat
```dart
// lib/screens/chatbot_screen.dart
import 'package:flutter/material.dart';
import '../models/chat_message.dart';
import '../services/chatbot_service.dart';

class ChatbotScreen extends StatefulWidget {
  const ChatbotScreen({super.key});

  @override
  State<ChatbotScreen> createState() => _ChatbotScreenState();
}

class _ChatbotScreenState extends State<ChatbotScreen> {
  final List<ChatMessage> _messages = [];
  final TextEditingController _controller = TextEditingController();
  final ChatbotService _chatbotService = ChatbotService();
  bool _isTyping = false;

  @override
  void initState() {
    super.initState();
    // Mensaje de bienvenida
    _messages.add(ChatMessage(
      id: '1',
      message: '¡Hola! Soy tu asistente de Joby. ¿En qué puedo ayudarte hoy?',
      isUser: false,
      timestamp: DateTime.now(),
    ));
  }

  Future<void> _sendMessage() async {
    if (_controller.text.isEmpty) return;

    final userMessage = ChatMessage(
      id: DateTime.now().toString(),
      message: _controller.text,
      isUser: true,
      timestamp: DateTime.now(),
    );

    setState(() {
      _messages.insert(0, userMessage);
      _isTyping = true;
    });

    final messageText = _controller.text;
    _controller.clear();

    try {
      // TODO: Obtener token del usuario autenticado
      final token = 'user-jwt-token';
      final response = await _chatbotService.sendMessage(messageText, token);

      final botMessage = ChatMessage(
        id: DateTime.now().toString(),
        message: response,
        isUser: false,
        timestamp: DateTime.now(),
      );

      setState(() {
        _messages.insert(0, botMessage);
        _isTyping = false;
      });
    } catch (e) {
      setState(() => _isTyping = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Row(
          children: const [
            Icon(Icons.smart_toy),
            SizedBox(width: 8),
            Text('Asistente IA'),
          ],
        ),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () {
              setState(() => _messages.clear());
              // Agregar mensaje de bienvenida nuevamente
            },
          ),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              reverse: true,
              padding: const EdgeInsets.all(16),
              itemCount: _messages.length + (_isTyping ? 1 : 0),
              itemBuilder: (context, index) {
                if (_isTyping && index == 0) {
                  return _buildTypingIndicator();
                }
                final message = _messages[index - (_isTyping ? 1 : 0)];
                return _buildMessageBubble(message);
              },
            ),
          ),
          _buildInputArea(),
        ],
      ),
    );
  }

  Widget _buildMessageBubble(ChatMessage message) {
    return Align(
      alignment: message.isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.only(bottom: 12),
        padding: const EdgeInsets.all(12),
        constraints: BoxConstraints(
          maxWidth: MediaQuery.of(context).size.width * 0.7,
        ),
        decoration: BoxDecoration(
          color: message.isUser
              ? Colors.blue
              : Colors.grey.shade200,
          borderRadius: BorderRadius.circular(16),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              message.message,
              style: TextStyle(
                color: message.isUser ? Colors.white : Colors.black87,
              ),
            ),
            const SizedBox(height: 4),
            Text(
              _formatTime(message.timestamp),
              style: TextStyle(
                fontSize: 10,
                color: message.isUser
                    ? Colors.white70
                    : Colors.grey.shade600,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildTypingIndicator() {
    return Align(
      alignment: Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.only(bottom: 12),
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: Colors.grey.shade200,
          borderRadius: BorderRadius.circular(16),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: const [
            SizedBox(
              width: 40,
              child: Text('...', style: TextStyle(fontSize: 24)),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildInputArea() {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.1),
            blurRadius: 10,
            offset: const Offset(0, -5),
          ),
        ],
      ),
      child: SafeArea(
        child: Row(
          children: [
            Expanded(
              child: TextField(
                controller: _controller,
                decoration: InputDecoration(
                  hintText: 'Escribe tu mensaje...',
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(24),
                  ),
                  contentPadding: const EdgeInsets.symmetric(
                    horizontal: 16,
                    vertical: 12,
                  ),
                ),
                onSubmitted: (_) => _sendMessage(),
              ),
            ),
            const SizedBox(width: 8),
            FloatingActionButton(
              onPressed: _sendMessage,
              child: const Icon(Icons.send),
            ),
          ],
        ),
      ),
    );
  }

  String _formatTime(DateTime time) {
    return '${time.hour}:${time.minute.toString().padLeft(2, '0')}';
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }
}
```

## Prompts Sugeridos

### Para Recomendaciones
```
Analiza el perfil del usuario y recomienda los 3 mejores trabajos.
Para cada trabajo, explica:
1. Por qué es una buena opción
2. Compatibilidad con habilidades
3. Áreas de mejora antes de aplicar
```

### Para Mejorar Perfil
```
Revisa el perfil del usuario y sugiere mejoras específicas:
1. Habilidades que debería añadir
2. Cómo mejorar la descripción de experiencia
3. Certificaciones recomendadas
```

### Para Preparar Entrevista
```
El usuario aplicó al trabajo: {job_title}
Genera:
1. 5 preguntas probables en la entrevista
2. Respuestas sugeridas
3. Consejos específicos para esta empresa
```

## Mejores Prácticas

1. **Contexto**: Siempre incluir el perfil del usuario en el contexto
2. **Límites**: Establecer límites de tokens para controlar costos
3. **Caché**: Guardar respuestas comunes para reducir llamadas a la API
4. **Privacidad**: No exponer datos sensibles en los logs
5. **Fallback**: Tener respuestas predefinidas si la API falla
6. **Rate Limiting**: Limitar número de mensajes por usuario

## Costos Estimados

### OpenAI GPT-4
- Input: $0.03 por 1K tokens
- Output: $0.06 por 1K tokens
- Promedio por conversación: ~1000 tokens = $0.09

### Google Gemini Pro
- Gratis hasta 60 peticiones por minuto
- Costo menor que GPT-4 en planes pagos

## Próximos Pasos

1. Configurar cuenta de OpenAI o Google AI
2. Implementar endpoints en Django
3. Crear interfaz de chat en Flutter
4. Añadir historial de conversaciones
5. Implementar sistema de recomendaciones avanzado
6. Agregar análisis de compatibilidad trabajo-usuario
7. Integrar con notificaciones push

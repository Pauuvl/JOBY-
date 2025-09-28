class Job {
  final int id;
  final String title;
  final String company;
  final String location;
  final String salary;
  final String description;
  final String requirements;
  final String type; // Remote, On-site, Hybrid
  final DateTime postedDate;

  Job({
    required this.id,
    required this.title,
    required this.company,
    required this.location,
    required this.salary,
    required this.description,
    required this.requirements,
    required this.type,
    required this.postedDate,
  });
}
# 🚀 Joby - Tu Compañero de Búsqueda de Empleo

**Joby** es una aplicación móvil innovadora diseñada para revolucionar la búsqueda de empleo. Combina gamificación, inteligencia artificial y una experiencia de usuario excepcional para ayudar a los candidatos a encontrar su trabajo ideal de manera más efectiva y motivadora.

## ✨ Características Principales

### 📱 Experiencia de Usuario Completa
- **Búsqueda Inteligente**: Encuentra trabajos según tu perfil, habilidades y preferencias
- **Detalles Completos**: Visualiza toda la información de cada trabajo (descripción, requisitos, beneficios, salario)
- **Aplicación Rápida**: Aplica a trabajos con un solo click
- **Favoritos**: Guarda trabajos para revisar más tarde

### 🔥 Sistema de Rachas (Gamificación)
Inspirado en apps exitosas como Duolingo y Streak (de la imagen P-03), Joby incluye:
- **Rachas Diarias**: Mantén una racha activa realizando actividades
- **Sistema de Puntos**: Gana puntos por aplicar a trabajos, actualizar tu perfil, etc.
- **Insignias**: Desbloquea logros especiales
- **Motivación Continua**: Notificaciones para mantener tu racha activa

#### Actividades que Suman Puntos:
- ✅ Ingreso diario: **+10 puntos**
- ✅ Aplicar a un trabajo: **+20 puntos**
- ✅ Actualizar perfil: **+15 puntos**
- ✅ Referir un amigo: **+30 puntos**

#### Insignias Disponibles:
- 🔥 **7 Días de Racha**: Mantén 7 días consecutivos
- 🏆 **Racha de 1 Mes**: 30 días consecutivos activo
- 🚀 **Primera Postulación**: Aplica a tus primeros 5 trabajos
- ⭐ **Centurión**: Alcanza 100 puntos totales

### 👤 Perfil Personalizable
- Edita tu información personal
- Agrega/elimina habilidades
- Describe tu experiencia y educación
- Sube tu CV (próximamente)
- Foto de perfil personalizable

### 📊 Estadísticas y Seguimiento
- Historial de aplicaciones
- Trabajos guardados
- Progreso de rachas
- Actividades recientes

## 🛠️ Tecnologías (Stack Actual y Planeado)

### Frontend (✅ Implementado)
- **Flutter 3.9+** - Framework multiplataforma
- **Dart** - Lenguaje de programación

### Backend (🚧 En desarrollo)
- **Django REST Framework** - API REST
- **PostgreSQL** - Base de datos relacional
- **JWT** - Autenticación segura
- **Docker** - Containerización

### Notificaciones (📅 Planeado)
- **Firebase Cloud Messaging** - Push notifications
- **Notificaciones de nuevos trabajos** compatibles
- **Recordatorios de racha diaria**

## 🚀 Instalación y Uso

### Prerrequisitos
```bash
Flutter SDK 3.9 o superior
Dart SDK 3.0 o superior
Android Studio / VS Code
```

### Clonar el Repositorio
```bash
git clone https://github.com/Pauuvl/JOBY-.git
cd JOBY-
```

### Instalar Dependencias
```bash
flutter pub get
```

### Ejecutar la Aplicación
```bash
flutter run
```

### Compilar para Producción
```bash
# Android
flutter build apk --release

# iOS
flutter build ios --release
```

## 📂 Estructura del Proyecto

```
lib/
├── main.dart                    # Punto de entrada
├── models/                      # Modelos de datos
│   ├── job.dart                # Modelo de trabajo
│   ├── user.dart               # Modelo de usuario
│   └── streak.dart             # Modelo de rachas
├── screens/                     # Pantallas de la app
│   ├── login_screen.dart       # Pantalla de login
│   ├── home_screen.dart        # Pantalla principal
│   ├── job_search_screen.dart  # Búsqueda de trabajos
│   ├── job_detail_screen.dart  # Detalles del trabajo
│   ├── profile_screen.dart     # Perfil del usuario
│   ├── edit_profile_screen.dart # Editar perfil
│   └── streak_screen.dart      # Rachas y gamificación
└── services/                    # Servicios y lógica de negocio
    └── streak_service.dart     # Servicio de rachas
```

## 🎯 Roadmap

### Fase 1: MVP Frontend ✅ (Completado)
- [x] Sistema de navegación
- [x] Búsqueda y listado de trabajos
- [x] Detalles de trabajos
- [x] Perfil de usuario
- [x] Sistema de rachas
- [x] Edición de perfil

### Fase 2: Backend y Base de Datos (En Desarrollo)
- [ ] API REST con Django
- [ ] Base de datos PostgreSQL
- [ ] Autenticación JWT
- [ ] Endpoints CRUD para trabajos y usuarios
- [ ] Sistema de aplicaciones

### Fase 3: Integración
- [ ] Conectar Flutter con API
- [ ] Sincronización de datos
- [ ] Caché local
- [ ] Manejo de estado (Provider/Riverpod/Bloc)

### Fase 4: Notificaciones
- [ ] Firebase Cloud Messaging
- [ ] Notificaciones push
- [ ] Notificaciones programadas para rachas
- [ ] Alertas de nuevos trabajos

### Fase 5: Características Avanzadas
- [ ] Sistema de referidos


## 🎨 Diseño

El diseño de Joby se inspira en:
- **Material Design 3** para consistencia
- **Apps de gamificación** como Duolingo
- **Plataformas de empleo** modernas como LinkedIn
- **Concepto P-03 "Streak: Mobile Service"** de Magneto


## 👥 Autores

-Cristian Cabarcas , Paulina Velazquez , Yilmar Murillo , Fabian Buritica



---

**¿Listo para encontrar tu próximo trabajo? ¡Descarga Joby y comienza tu racha hoy! 🔥**

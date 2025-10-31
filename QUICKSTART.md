# 🚀 Quick Start Guide - Joby

## Ejecución Rápida

```bash
# 1. Clonar el proyecto
git clone https://github.com/Pauuvl/JOBY-.git
cd JOBY-

# 2. Instalar dependencias
flutter pub get

# 3. Ejecutar la app
flutter run
```

## 📱 Probar la Aplicación

### 1. Login
- Email: cualquier email
- Password: cualquier password
- Click en "Iniciar Sesión"

### 2. Explorar Trabajos
- **Tab Inicio**: Ver trabajos destacados
- **Tab Buscar**: Buscar trabajos específicos
- **Click en trabajo**: Ver detalles completos
- **Botón "Aplicar ahora"**: Aplicar al trabajo (+20 puntos)

### 3. Sistema de Rachas
- **Perfil** → **Ver mis Rachas**
- Ver tu racha actual, puntos e insignias
- Click en "Registrar Actividad (Demo)" para probar
- Ganar puntos y desbloquear insignias

### 4. Editar Perfil
- **Perfil** → **Icono Editar** (arriba derecha)
- Modificar nombre, email, teléfono, ubicación
- Agregar experiencia y educación
- Añadir/eliminar habilidades
- Click en "Guardar Cambios"

## 🎮 Probar Sistema de Gamificación

### Ganar Puntos:
1. **Aplicar a trabajo**: +20 puntos
2. **Actividad diaria** (demo): +10 puntos
3. **Actualizar perfil**: +15 puntos (automático al guardar)

### Desbloquear Insignias:
- 🔥 **7 Días de Racha**: Mantén 7 días (usa el botón demo 7 veces)
- 🚀 **Primera Postulación**: Aplica a 5 trabajos
- ⭐ **Centurión**: Alcanza 100 puntos

## 📂 Estructura de Navegación

```
App
├── LoginScreen
└── HomeScreen (Bottom Nav)
    ├── HomeTab
    │   └── JobDetailScreen (click en trabajo)
    ├── JobSearchScreen
    │   └── JobDetailScreen (click en trabajo)
    └── ProfileScreen
        ├── EditProfileScreen (click en editar)
        └── StreakScreen (click en "Ver mis Rachas")
```

## 🎯 Features Disponibles Ahora

✅ Login funcional (simulado)
✅ 3 trabajos de ejemplo
✅ Búsqueda de trabajos
✅ Detalles completos de trabajos
✅ Aplicar a trabajos
✅ Guardar favoritos (UI)
✅ Sistema de rachas completo
✅ Puntos e insignias
✅ Edición de perfil
✅ Agregar/quitar habilidades

## 🔜 Próximamente (Requiere Backend)

⏳ Autenticación real
⏳ Trabajos desde base de datos
⏳ Aplicaciones persistentes
⏳ Favoritos guardados
⏳ Chatbot con IA
⏳ Notificaciones push
⏳ Sincronización en la nube

## 🐛 Debug Tips

### App no ejecuta:
```bash
flutter clean
flutter pub get
flutter run
```

### Problemas de build:
```bash
# Android
cd android
./gradlew clean
cd ..
flutter run

# iOS
cd ios
pod install
cd ..
flutter run
```

### Hot reload:
- Presiona `r` en la terminal
- O guarda el archivo en el editor

## 📱 Dispositivos Soportados

- ✅ Android (5.0+)
- ✅ iOS (11.0+)
- ✅ Emuladores
- ✅ Dispositivos físicos

## 💡 Tips de Desarrollo

1. **Hot Reload**: Guarda archivos para ver cambios instantáneos
2. **Debug**: Usa `print()` o debugger de VS Code
3. **Widgets**: Inspecciona con Flutter DevTools
4. **Errores**: Lee la consola, los errores son descriptivos

## 📚 Archivos Importantes

- `lib/main.dart` - Punto de entrada
- `lib/screens/` - Todas las pantallas
- `lib/models/` - Modelos de datos
- `lib/services/` - Lógica de negocio
- `README.md` - Documentación completa
- `BACKEND_ARCHITECTURE.md` - Guía de backend
- `CHATBOT_IMPLEMENTATION.md` - Guía de IA
- `PUSH_NOTIFICATIONS.md` - Guía de notificaciones

## 🎨 Personalización

### Cambiar colores:
```dart
// lib/main.dart
colorScheme: ColorScheme.fromSeed(
  seedColor: Colors.blue, // Cambia aquí
),
```

### Cambiar nombre de la app:
```yaml
# pubspec.yaml
name: joby  # Tu nombre aquí
```

## ⚡ Comandos Útiles

```bash
# Ver dispositivos disponibles
flutter devices

# Ejecutar en dispositivo específico
flutter run -d device_id

# Build de producción
flutter build apk --release  # Android
flutter build ios --release  # iOS

# Analizar código
flutter analyze

# Ejecutar tests
flutter test

# Ver dependencias desactualizadas
flutter pub outdated
```

## 🆘 Soporte

¿Problemas? Revisa:
1. `flutter doctor` para verificar instalación
2. Logs en la consola
3. Documentación en README.md
4. Issues en GitHub

## 🎉 ¡Listo para Desarrollar!

Ya tienes todo configurado. ¡Empieza a agregar funcionalidades o conectar el backend!

**Happy Coding! 🚀**

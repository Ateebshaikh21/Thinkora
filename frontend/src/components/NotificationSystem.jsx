import React, { useState, useEffect } from "react";

const NotificationSystem = () => {
  const [notifications, setNotifications] = useState([]);

  const addNotification = (message, type = "success", duration = 3000) => {
    const id = Date.now();
    const notification = { id, message, type, duration };

    setNotifications((prev) => [...prev, notification]);

    setTimeout(() => {
      removeNotification(id);
    }, duration);
  };

  const removeNotification = (id) => {
    setNotifications((prev) => prev.filter((notif) => notif.id !== id));
  };

  // Expose addNotification globally
  useEffect(() => {
    window.showNotification = addNotification;
    return () => {
      delete window.showNotification;
    };
  }, []);

  const getNotificationStyles = (type) => {
    const baseStyles =
      "fixed top-4 right-4 bg-white border-l-4 rounded-lg shadow-lg p-4 max-w-sm z-50 transform transition-all duration-300";

    switch (type) {
      case "success":
        return `${baseStyles} border-green-500`;
      case "error":
        return `${baseStyles} border-red-500`;
      case "warning":
        return `${baseStyles} border-yellow-500`;
      case "info":
        return `${baseStyles} border-blue-500`;
      default:
        return `${baseStyles} border-gray-500`;
    }
  };

  const getIcon = (type) => {
    switch (type) {
      case "success":
        return "✅";
      case "error":
        return "❌";
      case "warning":
        return "⚠️";
      case "info":
        return "ℹ️";
      default:
        return "📢";
    }
  };

  return (
    <div className="notification-container">
      {notifications.map((notification, index) => (
        <div
          key={notification.id}
          className={getNotificationStyles(notification.type)}
          style={{ top: `${1 + index * 5}rem` }}
        >
          <div className="flex items-center">
            <span className="text-xl mr-3">{getIcon(notification.type)}</span>
            <div className="flex-1">
              <p className="text-gray-800 font-medium">
                {notification.message}
              </p>
            </div>
            <button
              onClick={() => removeNotification(notification.id)}
              className="ml-3 text-gray-400 hover:text-gray-600 transition-colors"
            >
              ✕
            </button>
          </div>
        </div>
      ))}
    </div>
  );
};

export default NotificationSystem;

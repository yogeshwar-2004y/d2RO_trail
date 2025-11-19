<template>
  <div
    class="sidebar-container"
    :class="{ open: isOpen, collapsed: isCollapsed }"
  >
    <!-- Sidebar Content -->
    <div class="sidebar-content" :class="{ collapsed: isCollapsed }">
      <!-- Collapse/Expand Button -->
      <div class="collapse-section">
        <button class="collapse-btn" @click="toggleCollapse">
          <svg
            v-if="isCollapsed"
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <polyline points="9 18 15 12 9 6"></polyline>
          </svg>
          <svg
            v-else
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <polyline points="15 18 9 12 15 6"></polyline>
          </svg>
        </button>
      </div>

      <!-- User Info Section -->
      <div class="user-info-section">
        <div class="user-avatar">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="32"
            height="32"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
            <circle cx="12" cy="7" r="4"></circle>
          </svg>
        </div>
        <div class="user-details" v-if="!isCollapsed">
          <h4>{{ userInfo.name }}</h4>
          <p>{{ userInfo.role }}</p>
          <p class="user-id">ID: {{ userInfo.id }}</p>
        </div>
      </div>

      <!-- Navigation Cards Section -->
      <div class="navigation-section">
        <h3 v-if="!isCollapsed">Navigation</h3>
        <div class="nav-cards">
          <div
            v-for="card in roleBasedCards"
            :key="card.id"
            class="nav-card"
            :class="{ collapsed: isCollapsed }"
            @click="navigateToPage(card.route)"
          >
            <div class="card-icon">
              <component :is="card.icon" />
            </div>
            <div class="card-title" v-if="!isCollapsed">
              {{ card.title }}
            </div>
          </div>
        </div>
      </div>

      <!-- Profile/Settings Section -->
      <div class="profile-section">
        <h3 v-if="!isCollapsed">Account</h3>
        <div class="profile-menu">
          <div
            class="profile-item notification-item-wrapper"
            @click="openNotifications"
            :class="{ 'has-notifications': unreadCount > 0 }"
          >
            <div class="notification-icon-wrapper">
              <NotificationIcon />
              <span v-if="unreadCount > 0" class="notification-count-badge">{{
                unreadCount > 9 ? "9+" : unreadCount
              }}</span>
            </div>
            <span v-if="!isCollapsed">Notifications</span>
          </div>

          <!-- <div class="profile-item" @click="handleProfileAction('profile')">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
            <span v-if="!isCollapsed">Profile</span>
          </div> -->

          <div
            class="profile-item"
            @click="handleProfileAction('tech-support')"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M9 12l2 2 4-4"></path>
              <path
                d="M21 12c.552 0 1-.448 1-1V5c0-.552-.448-1-1-1H3c-.552 0-1 .448-1 1v6c0 .552.448 1 1 1h18z"
              ></path>
              <path
                d="M3 12h18v6c0 .552-.448 1-1 1H4c-.552 0-1-.448-1-1v-6z"
              ></path>
            </svg>
            <span v-if="!isCollapsed">Tech Support</span>
          </div>

          <!-- Tech Support Requests - Admin Only -->
          <div
            v-if="isAdmin"
            class="profile-item"
            @click="handleProfileAction('tech-support-requests')"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path
                d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"
              ></path>
              <polyline points="14 2 14 8 20 8"></polyline>
              <line x1="16" y1="13" x2="8" y2="13"></line>
              <line x1="16" y1="17" x2="8" y2="17"></line>
              <polyline points="10 9 9 9 8 9"></polyline>
            </svg>
            <span v-if="!isCollapsed">Tech Support Requests</span>
          </div>

          <div
            class="profile-item password-item"
            @click="togglePasswordSubmenu"
            :class="{ active: showPasswordSubmenu }"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
              <circle cx="12" cy="16" r="1"></circle>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>
            <span v-if="!isCollapsed">Passwords</span>
            <svg
              v-if="!isCollapsed"
              class="dropdown-arrow"
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </div>

          <!-- Password Submenu -->
          <div
            class="password-submenu"
            v-if="showPasswordSubmenu && !isCollapsed"
          >
            <div
              class="submenu-item"
              @click="handleProfileAction('change-login-password')"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                <circle cx="12" cy="16" r="1"></circle>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
              </svg>
              <span>Login Password</span>
            </div>
            <div
              class="submenu-item"
              @click="handleProfileAction('change-signature-password')"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <path d="M12 20h9"></path>
                <path
                  d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"
                ></path>
              </svg>
              <span>Signature Password</span>
            </div>
          </div>

          <div class="profile-divider"></div>

          <div class="profile-item logout-item" @click="handleLogout">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
              <polyline points="16 17 21 12 16 7"></polyline>
              <line x1="21" y1="12" x2="9" y2="12"></line>
            </svg>
            <span v-if="!isCollapsed">Logout</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Password Change Modal - Teleported to body for proper centering -->
    <Teleport to="body">
      <PasswordChangeModal
        :isOpen="isPasswordModalOpen"
        :passwordType="passwordType"
        @close="closePasswordModal"
      />
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import { userStore } from "@/stores/userStore";
import PasswordChangeModal from "@/components/PasswordChangeModal.vue";

const emit = defineEmits(["open-notifications", "sidebar-state-changed"]);

// Import icon components
import HomeIcon from "./icons/HomeIcon.vue";
import DocumentIcon from "./icons/DocumentIcon.vue";
import MemoIcon from "./icons/MemoIcon.vue";
import ReportIcon from "./icons/ReportIcon.vue";
import UserIcon from "./icons/UserIcon.vue";
import AssignIcon from "./icons/AssignIcon.vue";
import NotificationIcon from "./icons/NotificationIcon.vue";

const router = useRouter();

// Reactive data
const isOpen = ref(true); // Collapsed by default
const isCollapsed = ref(true); // Collapsed by default
const showPasswordSubmenu = ref(false);
const isPasswordModalOpen = ref(false);
const passwordType = ref("login");
const unreadCount = ref(0);
let notificationRefreshInterval = null;

// Computed properties
const userInfo = computed(() => {
  return userStore.getters.currentUser() || { name: "User", role: "Unknown" };
});

const isAdmin = computed(() => {
  const userRole = userStore.getters.currentUserRole();
  const roleName = userStore.getters.roleName();
  return userRole === 1 || roleName?.toLowerCase() === "admin";
});

// Role-based cards configuration
const roleBasedCards = computed(() => {
  // const userRole = userInfo.value.role?.toLowerCase()
  const userRole = userInfo.value.role?.toLowerCase().replace(/\s+/g, "");

  console.log("User Role:", userRole); // Debugging line

  const cardDefinitions = {
    admin: [
      { id: "home", title: "Home", route: "HomePageAdmin", icon: HomeIcon },
      {
        id: "user activities",
        title: "User Activities",
        route: "UserActivities",
        icon: UserIcon,
      },
      {
        id: "documents",
        title: "Documents",
        route: "ProjectsDashboard",
        icon: DocumentIcon,
      },
      { id: "memos", title: "Memos", route: "MemoDashboard", icon: MemoIcon },
      {
        id: "reports",
        title: "Reports",
        route: "ReportDashboard",
        icon: ReportIcon,
      },
      // {
      //   id: "user activities",
      //   title: "User Activities",
      //   route: "UserActivities",
      //   icon: UserIcon,
      // },
    ],
    qareviewer: [
      { id: "home", title: "Home", route: "HomePageReviewer", icon: HomeIcon },
      {
        id: "documents",
        title: "Documents",
        route: "ProjectsDashboard",
        icon: DocumentIcon,
      },
      { id: "memos", title: "Memos", route: "MemoDashboard", icon: MemoIcon },
      {
        id: "reports",
        title: "Reports",
        route: "ReportDashboard",
        icon: ReportIcon,
      },
    ],
    qahead: [
      { id: "home", title: "Home", route: "HomePageQAHead", icon: HomeIcon },
      {
        id: "documents",
        title: "Documents",
        route: "ProjectsDashboard",
        icon: DocumentIcon,
      },
      { id: "memos", title: "Memos", route: "MemoDashboard", icon: MemoIcon },
      {
        id: "reports",
        title: "Reports",
        route: "ReportDashboard",
        icon: ReportIcon,
      },
    ],
    designhead: [
      {
        id: "home",
        title: "Home",
        route: "HomePageDesignHead",
        icon: HomeIcon,
      },
      {
        id: "documents",
        title: "Documents",
        route: "ProjectsDashboard",
        icon: DocumentIcon,
      },
      { id: "memos", title: "Memos", route: "MemoDashboard", icon: MemoIcon },
      {
        id: "reports",
        title: "Reports",
        route: "ReportDashboard",
        icon: ReportIcon,
      },
      {
        id: "assign",
        title: "Assign Projects",
        route: "ProjectsForAssigning",
        icon: AssignIcon,
      },
    ],
    designer: [
      { id: "home", title: "Home", route: "HomePageDesigner", icon: HomeIcon },
      {
        id: "documents",
        title: "Documents",
        route: "ProjectsDashboard",
        icon: DocumentIcon,
      },
      { id: "memos", title: "Memos", route: "MemoDashboard", icon: MemoIcon },
      {
        id: "reports",
        title: "Reports",
        route: "ReportDashboard",
        icon: ReportIcon,
      },
    ],
  };

  return cardDefinitions[userRole] || [];
});

// Methods
const toggleSidebar = () => {
  isOpen.value = !isOpen.value;
  if (!isOpen.value) {
    showPasswordSubmenu.value = false; // Close submenu when closing sidebar
  }
};

const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value;
  // Emit the state change to parent component for responsive layout
  emit("sidebar-state-changed", isCollapsed.value);
};

const navigateToPage = (routeName) => {
  router.push({ name: routeName });
  // Close sidebar after navigation on mobile
  if (window.innerWidth <= 768) {
    isOpen.value = false;
  }
};

const handleProfileAction = (action) => {
  switch (action) {
    case "profile":
      // Handle profile action
      console.log("Profile clicked");
      break;
    case "tech-support":
      // Navigate to tech support dashboard (shows user's requests) for all users including admin
      router.push({ name: "TechSupportUserDashboard" });

      // Close sidebar after navigation on mobile
      if (window.innerWidth <= 768) {
        isOpen.value = false;
      }
      break;
    case "tech-support-requests":
      // Navigate to tech support management page (admin only)
      router.push({ name: "TechSupportManagement" });

      // Close sidebar after navigation on mobile
      if (window.innerWidth <= 768) {
        isOpen.value = false;
      }
      break;
    case "change-login-password":
      passwordType.value = "login";
      isPasswordModalOpen.value = true;
      break;
    case "change-signature-password":
      passwordType.value = "signature";
      isPasswordModalOpen.value = true;
      break;
  }
};

const togglePasswordSubmenu = () => {
  showPasswordSubmenu.value = !showPasswordSubmenu.value;
};

const closePasswordModal = () => {
  isPasswordModalOpen.value = false;
};

const handleLogout = async () => {
  // Handle logout
  await userStore.actions.logout();
  router.push({ name: "login" });
};

const openNotifications = () => {
  emit("open-notifications");
};

const fetchUnreadCount = async () => {
  try {
    const currentUser = userStore.getters.currentUser();

    if (!currentUser || !currentUser.id) {
      return;
    }

    const response = await fetch(
      `/api/notifications/${currentUser.id}?limit=50&unread_only=true`
    );
    const data = await response.json();

    if (data.success) {
      unreadCount.value = data.notifications.length;
    }
  } catch (error) {
    console.error("Error fetching notification count:", error);
  }
};

// Initialize user store on mount
onMounted(() => {
  userStore.actions.initializeUser();
  fetchUnreadCount();
  // Refresh every 30 seconds
  notificationRefreshInterval = setInterval(fetchUnreadCount, 30000);
  // Emit initial sidebar state to parent
  emit("sidebar-state-changed", isCollapsed.value);
});

onUnmounted(() => {
  if (notificationRefreshInterval) {
    clearInterval(notificationRefreshInterval);
  }
});
</script>

<style scoped>
.sidebar-container {
  position: fixed;
  top: 0; /* Start from very top */
  left: 0;
  height: 100vh; /* Full height */
  z-index: 9999; /* Above all components */
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.sidebar-container:not(.open) {
  transform: translateX(-100%);
}

.sidebar-container.open {
  transform: translateX(0);
}

.sidebar-toggle {
  position: fixed;
  top: 30px; /* Position below header */
  left: 30px;
  background: #e74c3c; /* Bright red for visibility */
  border: 2px solid #fff; /* Thicker white border */
  color: white;
  width: 55px; /* Wider for text */
  height: 60px; /* Larger size */
  border-radius: 30px; /* Rounded rectangle */
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.7); /* Stronger shadow */
  transition: all 0.3s ease;
  z-index: 10000; /* Highest z-index */
  font-weight: bold;
  font-size: 14px; /* Text size */
}

.toggle-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.toggle-text {
  font-size: 12px;
  font-weight: bold;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

.sidebar-toggle:hover {
  background: #34495e;
  transform: scale(1.05);
}

.sidebar-content {
  width: 250px;
  height: 100vh; /* Full viewport height */
  background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
  color: white;
  display: flex;
  flex-direction: column;
  box-shadow: 4px 0 20px rgba(0, 0, 0, 0.3);
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.sidebar-content.collapsed {
  width: 50px;
}

/* User Info Section */
.user-info-section {
  display: flex;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  margin-bottom: 20px;
}

.user-avatar {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.user-details {
  margin-left: 12px;
  min-width: 0;
}

.user-details h4 {
  margin: 0 0 4px 0;
  font-size: 1rem;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-details p {
  margin: 0;
  font-size: 0.875rem;
  opacity: 0.8;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-details .user-id {
  margin-top: 2px;
  font-size: 0.75rem;
  opacity: 0.6;
  font-weight: 400;
}

/* Navigation Section */
.navigation-section {
  flex: 1;
  padding: 0 20px;
}

.navigation-section h3 {
  margin: 0 0 15px 0;
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  opacity: 0.8;
}

.nav-cards {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.nav-card {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid transparent;
}

.nav-card:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
  transform: translateX(4px);
}

.nav-card.collapsed {
  justify-content: center;
  padding: 12px;
}

.card-icon {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.card-title {
  margin-left: 12px;
  font-size: 0.875rem;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Profile Section */
.profile-section {
  padding: 0 20px 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  margin-top: 20px;
}

.profile-section h3 {
  margin: 20px 0 15px 0;
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  opacity: 0.8;
}

.profile-menu {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.profile-item {
  display: flex;
  align-items: center;
  padding: 12px 5px;
  cursor: pointer;
  transition: all 0.2s ease;
  border-radius: 6px;
  position: relative;
}

.profile-item:hover {
  /* background: rgba(255, 255, 255, 0.1); */
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
  transform: translateX(4px);
}

.profile-item svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.profile-item span {
  margin-left: 12px;
  font-size: 0.875rem;
  font-weight: 500;
}

.password-item {
  position: relative;
}

.password-item.active {
  background: rgba(255, 255, 255, 0.1);
}

.dropdown-arrow {
  margin-left: auto;
  transition: transform 0.2s ease;
}

.password-item.active .dropdown-arrow {
  transform: rotate(180deg);
}

.password-submenu {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 6px;
  margin: 4px 0 0 20px;
  padding: 8px 0;
  animation: slideDown 0.2s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.submenu-item {
  display: flex;
  align-items: center;
  padding: 8px 16px;
  cursor: pointer;
  transition: background-color 0.2s ease;
  border-radius: 4px;
  margin: 0 8px;
}

.submenu-item:hover {
  background: rgba(255, 255, 255, 0.1);
}

.submenu-item svg {
  width: 16px;
  height: 16px;
  margin-right: 8px;
}

.submenu-item span {
  font-size: 0.8rem;
  margin-left: 0;
}

.profile-divider {
  height: 1px;
  background: rgba(255, 255, 255, 0.1);
  margin: 12px 0;
}

.logout-item {
  color: #ff6b6b;
  margin-bottom: 8px;
}

.logout-item:hover {
  background: rgba(255, 107, 107, 0.1);
}

/* Notification Item Styling */
.notification-item-wrapper {
  position: relative;
}

.notification-icon-wrapper {
  position: relative;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.notification-count-badge {
  position: absolute;
  top: -6px;
  right: -6px;
  background: #dc3545;
  color: white;
  border-radius: 50%;
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 9px;
  font-weight: bold;
  border: 2px solid #2d3748;
}

.notification-item-wrapper.has-notifications {
  font-weight: 600;
}

/* Collapse Section */
.collapse-section {
  padding: 10px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  bottom: 50px;
}

.collapse-btn {
  width: 100%;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: white;
  padding: 5px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.collapse-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

/* Collapsed State Adjustments */
.sidebar-content.collapsed .user-info-section {
  justify-content: center;
  padding: 20px 10px;
}

.sidebar-content.collapsed .navigation-section,
.sidebar-content.collapsed .profile-section {
  padding: 0 10px;
}

.sidebar-content.collapsed .navigation-section h3,
.sidebar-content.collapsed .profile-section h3 {
  display: none;
}

.sidebar-content.collapsed .collapse-section {
  padding: 20px 10px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .sidebar-content {
    width: 100%;
  }

  .sidebar-toggle {
    left: 15px;
    top: 15px;
    width: 45px;
    height: 45px;
  }
}

/* Icon Components */
.document-icon,
.memo-icon,
.report-icon,
.user-icon,
.assign-icon {
  width: 24px;
  height: 24px;
}
</style>

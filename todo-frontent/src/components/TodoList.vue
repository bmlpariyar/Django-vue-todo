<template>
  <div class="container mx-auto p-4">
    <h1 class="text-3xl font-bold mb-4">Todo List</h1>

    <!-- If no current user, show login form -->
    <div v-if="!currentUser" class="mb-4">
      <input
        v-model="loginForm.username"
        type="text"
        placeholder="Username"
        class="mr-2 px-2 py-1 border rounded"
      />
      <input
        v-model="loginForm.password"
        type="password"
        placeholder="Password"
        class="mr-2 px-2 py-1 border rounded"
      />
      <button @click="login" class="bg-blue-500 text-white px-4 py-1 rounded">
        Login
      </button>
    </div>

    <!-- If logged in, show user information and todo input -->
    <div v-else>
      <p class="mb-4">
        Welcome, {{ currentUser.username }}!
        <button @click="logout" class="text-blue-500">Logout</button>
      </p>
      <div class="mb-4">
        <input
          v-model="newTodo.title"
          type="text"
          placeholder="Add a new todo title"
          class="w-full px-3 py-2 border rounded-lg mb-2"
        />
        <textarea
          v-model="newTodo.description"
          placeholder="Add a description"
          class="w-full px-3 py-2 border rounded-lg mb-2"
        ></textarea>
        <button
          @click="addTodo"
          class="bg-blue-500 text-white px-4 py-2 rounded-lg"
        >
          Add Todo
        </button>
      </div>

      <!-- Displaying list of todos -->
      <ul class="space-y-4">
        <li
          v-for="todo in todos"
          :key="todo.id"
          class="bg-white p-4 rounded-lg shadow"
        >
          <div class="flex items-center justify-between mb-2">
            <h2
              class="text-xl font-semibold"
              :class="{ 'line-through text-gray-400': todo.completed }"
            >
              {{ todo.title }}
            </h2>
            <span class="text-sm text-gray-500"
              >Created by: {{ todo.user.username }}</span
            >
          </div>
          <p
            class="text-gray-700 mb-2"
            :class="{ 'line-through text-gray-400': todo.completed }"
          >
            {{ todo.description }}
          </p>
          <div class="flex items-center justify-between">
            <div>
              <input
                type="checkbox"
                :checked="todo.completed"
                @change="toggleTodo(todo)"
                class="mr-2"
              />
              <span>{{ todo.completed ? "Completed" : "Pending" }}</span>
            </div>
            <div>
              <button @click="editTodo(todo)" class="text-blue-500 mr-2">
                Edit
              </button>
              <button @click="deleteTodo(todo)" class="text-red-500">
                Delete
              </button>
            </div>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import api from "../services/api";
import authService from "../services/auth";

export default {
  data() {
    return {
      todos: [],
      newTodo: {
        title: "",
        description: "",
      },
      currentUser: null,
      loginForm: {
        username: "",
        password: "",
      },
    };
  },
  methods: {
    // User login
    async login() {
      try {
        await authService.login(
          this.loginForm.username,
          this.loginForm.password
        );
        this.currentUser = authService.getCurrentUser();
        this.loginForm = { username: "", password: "" };
        this.fetchTodos();
      } catch (error) {
        console.error("Login failed:", error);
      }
    },
    // Logout user and clear data
    logout() {
      authService.logout();
      this.currentUser = null;
      this.todos = [];
    },
    // Fetch the list of todos from API
    async fetchTodos() {
      try {
        const response = await api.get("/api/todos"); // Automatically includes token in header
        this.todos = response.data;
      } catch (error) {
        console.error("Error fetching todos:", error);
      }
    },
    // Add a new todo
    async addTodo() {
      if (this.newTodo.title.trim()) {
        try {
          await api.post("/api/create_todo/", this.newTodo);
          this.newTodo = { title: "", description: "" };
          await this.fetchTodos();
        } catch (error) {
          console.error("Error adding todo:", error);
        }
      }
    },
    // Toggle todo completion
    async toggleTodo(todo) {
      try {
        await api.patch(`/api/update_todo/${todo.id}`, {
          completed: !todo.completed,
        });
        await this.fetchTodos();
      } catch (error) {
        console.error("Error updating todo:", error);
      }
    },
    // Edit todo (placeholder for edit functionality)
    async editTodo(todo) {
      console.log("Edit todo:", todo);
    },
    // Delete todo
    async deleteTodo(todo) {
      try {
        await api.delete(`/api/delete_todo/${todo.id}`);
        await this.fetchTodos();
      } catch (error) {
        console.error("Error deleting todo:", error);
      }
    },
  },
  mounted() {
    this.currentUser = authService.getCurrentUser();
    if (this.currentUser) {
      this.fetchTodos();
    }
  },
};
</script>

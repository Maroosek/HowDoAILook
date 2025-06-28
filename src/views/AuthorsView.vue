<template>
  <div class="outfit-bg">
    <div class="outfit-glass-container">
      <h1 class="text-2xl font-bold text-center mb-8" style="color:#a7a2ff;">Autorzy projektu</h1>
      <div class="authors-list">
        <div
          v-for="author in authors"
          :key="author.name"
          class="author-card"
        >
          <img
            :src="author.avatar"
            alt="avatar"
            class="avatar"
            v-if="author.avatar"
          />
          <div class="author-name">{{ author.name }}</div>
          <div class="author-role">{{ author.role }}</div>
          <a
            :href="author.linkedin"
            target="_blank"
            rel="noopener noreferrer"
            class="author-link"
          >LinkedIn</a>
          <a
            :href="author.github"
            target="_blank"
            rel="noopener noreferrer"
            class="author-link"
          >Github</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const authors = [
  {
    name: "Marek Korkosz",
    role: "Frontend Developer",
    avatar: "https://i.pinimg.com/736x/02/51/48/0251481d696d33984f6e9c0bacbf0ccc.jpg",
    linkedin: "https://www.linkedin.com/in/marek-korkosz-474a882a3/",
    github: "https://github.com/Maroosek"

  },
  {
    name: "Jakub Kostka",
    role: "Fullstack & AI",
    avatar: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTYLQYOXbWHfxSPBD6CD7oMzYfqh5H9wcHM-Q&s",
    linkedin: "https://www.linkedin.com/in/jakub-kostka-300499249/",
    github: "https://github.com/j3k01"

  }
]
</script>

<style scoped>
.authors-list {
  min-width: 300px;
  max-width: 420px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  align-items: center;
}
.author-card {
  min-width: 140px;
  max-width: 280px;
  min-height: 150px;
  max-height: 250px;
  border-radius: 30px;
  background: rgba(255,255,255,0.13);
  box-shadow: 0 2px 18px 0 #23234725;
  padding: 2.5rem 2.5rem 2.5rem 2.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 1px solid rgba(185,185,255,0.09);
}
.avatar {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  border: 2.5px solid #a7a2ff;
  object-fit: cover;
  margin-bottom: 10px;
  background: white;
}
.author-name {
  font-size: 1.18rem;
  font-weight: 700;
  color: #d7d5ff;
  margin-bottom: 2px;
  text-align: center;
}
.author-role {
  font-size: 1rem;
  color: #b7b4d0;
  margin-bottom: 9px;
  text-align: center;
}
.author-link {
  color: #fff;
  margin-bottom: 4px;
  background: linear-gradient(90deg, #667eea 0%, #f093fb 100%);
  padding: 0.38rem 1.1rem;
  border-radius: 12px;
  font-weight: 500;
  text-decoration: none;
  transition: background .17s, box-shadow .17s;
  box-shadow: 0 1px 5px 0 #23234722;
}
.author-link:hover {
  background: linear-gradient(90deg, #7f53ac 0%, #647dee 100%);
  color: #f3f3f3;
}

</style>

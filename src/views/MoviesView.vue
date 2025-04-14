<template>
	<div class="movies-view">
		<h1 class="mb-4">My Movie Collection</h1>

		<div v-if="loading" class="text-center">
			<p>Loading movies...</p>
		</div>

		<div v-else-if="error" class="alert alert-danger">
			{{ error }}
		</div>

		<div v-else-if="movies.length === 0" class="text-center">
			<p>No movies found. Add some movies to get started!</p>
			<router-link to="/movies/create" class="btn btn-primary"
				>Add a Movie</router-link
			>
		</div>

		<div v-else class="row row-cols-1 row-cols-md-3 g-4">
			<div v-for="movie in movies" :key="movie.id" class="col">
				<div class="card h-100">
					<img
						:src="movie.poster"
						class="card-img-top"
						:alt="movie.title"
					/>
					<div class="card-body">
						<h5 class="card-title">{{ movie.title }}</h5>
						<p class="card-text">{{ movie.description }}</p>
					</div>
					<div class="card-footer">
						<small class="text-muted"
							>Added on {{ formatDate(movie.created_at) }}</small
						>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, onMounted } from "vue";

let movies = ref([]);
let loading = ref(true);
let error = ref(null);

function fetchMovies() {
	loading.value = true;
	error.value = null;

	fetch("/api/v1/movies")
		.then((response) => {
			if (!response.ok) {
				throw new Error("Failed to fetch movies");
			}
			return response.json();
		})
		.then((data) => {
			console.log("Movies retrieved:", data);
			movies.value = data.movies;
			loading.value = false;
		})
		.catch((err) => {
			console.error("Error fetching movies:", err);
			error.value =
				"There was an error loading the movies. Please try again later.";
			loading.value = false;
		});
}

function formatDate(dateString) {
	const options = { year: "numeric", month: "short", day: "numeric" };
	return new Date(dateString).toLocaleDateString(undefined, options);
}

onMounted(() => {
	fetchMovies();
});
</script>

<style scoped>
.movies-view {
	padding: 20px;
}

h1 {
	color: #333;
}

.card-img-top {
	height: 300px;
	object-fit: cover;
}
</style>

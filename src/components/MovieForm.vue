<template>
	<div class="movie-form-container">
		<form id="movieForm" @submit.prevent="saveMovie">
			<div class="form-group mb-3">
				<label for="title" class="form-label">Movie Title</label>
				<input type="text" name="title" class="form-control" />
			</div>

			<div class="form-group mb-3">
				<label for="description" class="form-label"
					>Movie Description</label
				>
				<textarea
					name="description"
					class="form-control"
					rows="4"
				></textarea>
			</div>

			<div class="form-group mb-3">
				<label for="poster" class="form-label">Movie Poster</label>
				<input type="file" name="poster" class="form-control" />
			</div>

			<button type="submit" class="btn btn-primary">Add Movie</button>
		</form>

		<div v-if="successMessage" class="alert alert-success mt-3">
			{{ successMessage }}
		</div>

		<div v-if="errors.length > 0" class="alert alert-danger mt-3">
			<ul>
				<li v-for="(error, index) in errors" :key="index">
					{{ error }}
				</li>
			</ul>
		</div>
	</div>
</template>

<script setup>
import { ref, onMounted } from "vue";

let csrf_token = ref("");
let successMessage = ref("");
let errors = ref([]);

function getCsrfToken() {
	fetch("/api/v1/csrf-token")
		.then((response) => response.json())
		.then((data) => {
			console.log("CSRF Token received");
			csrf_token.value = data.csrf_token;
		})
		.catch((error) => {
			console.error("Error fetching CSRF token:", error);
		});
}

function saveMovie() {
	// Reset messages
	successMessage.value = "";
	errors.value = [];

	let movieForm = document.getElementById("movieForm");
	let form_data = new FormData(movieForm);

	fetch("/api/v1/movies", {
		method: "POST",
		body: form_data,
		headers: {
			"X-CSRFToken": csrf_token.value,
		},
	})
		.then(function (response) {
			return response.json();
		})
		.then(function (data) {
			console.log(data);
			if (data.errors) {
				errors.value = data.errors;
			} else {
				successMessage.value = data.message;
				// Reset form
				movieForm.reset();
			}
		})
		.catch(function (error) {
			console.error("Error submitting form:", error);
		});
}

onMounted(() => {
	getCsrfToken();
});
</script>

<style scoped>
.movie-form-container {
	max-width: 600px;
	margin: 0 auto;
	padding: 20px;
}
</style>

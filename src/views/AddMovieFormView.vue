<template>
	<div class="add-movie-view">
		<h1>Add a New Movie</h1>
		<p>Fill out the form below to add a new movie to the database.</p>
		<MovieForm />
	</div>
</template>

<script setup>
import MovieForm from "@/components/MovieForm.vue";
</script>

<style scoped>
.add-movie-view {
	padding: 20px;
}

h1 {
	margin-bottom: 20px;
	color: #333;
}
</style>

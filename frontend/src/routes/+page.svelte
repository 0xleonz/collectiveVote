<script>
  import Header from '$lib/components/Header.svelte';
  import Footer from '$lib/components/Footer.svelte';

  let name = 'Mundo';
</script>

<Header title="Bienvenido!" />

<main class="p-6">
  <h2>¡Hola, {name}!</h2>
  <p>Este es tu nuevo frontend con SvelteKit.</p>
</main>

<Footer />

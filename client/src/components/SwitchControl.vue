<template>
  <div>
    <button @click="toggleBulb">Toggle Bulb</button>
  </div>
</template>

<script>

export default {
  data() {
    return {
      client: null,
      publishTopic: 'light',
      publishPayloads: {
        on: 'ON',
        off: 'OFF',
      },
    };
  },
  methods: {
 
 }
};
</script>

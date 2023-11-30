<template>
  <div>
    <div class="bulb" :class="{ 'glow': isOn }"></div>
  </div>
</template>

<script>
import mqtt from "mqtt";

export default {
  data() {
    return {
      isOn: false,
      client: null,
      subscriptionTopic: 'light',
    };
  },

  methods: {
    createMqttClient() {
      const brokerOptions = {
        protocol: 'ws',
        host: 'broker.emqx.io',
        port: 8083,
        clientId: `switch_client_${Math.random().toString(16).substring(2, 8)}`,
        clean: true,
        connectTimeout: 30 * 1000,
        reconnectPeriod: 4000,
        username: 'emqx_test',
        password: 'emqx_test',
      };
      
      this.client = mqtt.connect(`ws://${brokerOptions.host}:${brokerOptions.port}/mqtt`, brokerOptions);

      this.client.on('connect', () => {
        console.log('Switch Control connected to MQTT');
      });

      this.client.on('reconnect', () => {
        console.log('Switch Control reconnected to MQTT');
      });

      this.client.on('error', (error) => {
        console.error('Switch Control MQTT error:', error);
      });
    },
  },

  created() {
    this.createMqttClient();
  },

  beforeUnmount() {
    if (this.client) {
      this.client.end();
    }
  },
};
</script>

<style scoped>
.bulb {
  width: 100px;
  height: 100px;
  background-color: #ccc;
  border-radius: 50%;
  margin: 20px;
  transition: background-color 0.5s;
}

.glow {
  background-color: yellow;
}
</style>

<template>
  <div>
    <div class="bulb" :class="{ 'glow': isOn }"></div>
  </div>
</template>

<script>
import mqtt from "mqtt";
import axios from "axios";

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
        clientId: `bulb_client_${Math.random().toString(16).substring(2, 8)}`,
        clean: true,
        connectTimeout: 30 * 1000,
        reconnectPeriod: 4000,
        username: 'emqx_test',
        password: 'emqx_test',
      };
      
      this.client = mqtt.connect(`ws://${brokerOptions.host}:${brokerOptions.port}/mqtt`, brokerOptions);

      this.client.on('connect', () => {
        console.log('Bulb connected to MQTT');
        this.subscribeToTopic();
      });

      this.client.on('message', (topic, message) => {
        if (topic === this.subscriptionTopic) {
          this.handleMessage(message.toString());
        }
      });

      this.client.on('reconnect', () => {
        console.log('Bulb reconnected to MQTT');
      });

      this.client.on('error', (error) => {
        console.error('Bulb MQTT error:', error);
      });
    },

    subscribeToTopic() {
      this.client.subscribe(this.subscriptionTopic, (error) => {
        if (error) {
          console.log('Subscribe to topic error', error);
        } else {
          console.log('Bulb subscribed to topic:', this.subscriptionTopic);
        }
      });
    },

    handleMessage(message) {
      console.log('Received message:', message);
      this.isOn = message === 'ON';
    },


    async fetchInitialStatus() {
    try {
      // Make HTTP GET request to FastAPI endpoint to fetch initial status
      var id="65693c49d79ad6fc00b46051";
      const response = await axios.get(`http://localhost:8000/api/client/read/${id}`);
      console.log(response.data,'response');
      this.isOn = response.data === 'ON';
    } catch (error) {
      console.error("Failed to fetch initial status:", error);
    }
  },
  },
  

  created() {
  console.log('first');
    this.fetchInitialStatus();
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

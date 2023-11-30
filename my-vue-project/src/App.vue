<template>
  <div>
    <button @click="toggleButton">Toggle Button</button>
    <p v-if="buttonStatus">Button is ON</p>
    <p v-else>Button is OFF</p>
  </div>
</template>

<script>
import mqtt from "mqtt";

export default {
  data() {
    return {
      buttonStatus: false,
      connection: {
        protocol: "ws",
        host: "broker.emqx.io",
        port: 8083,
        endpoint: "/mqtt",
        clean: true,
        connectTimeout: 30 * 1000,
        reconnectPeriod: 4000,
        clientId: "emqx_vue_" + Math.random().toString(16).substring(2, 8),
        username: "emqx_test",
        password: "emqx_test",
      },
      subscription: {
        topic: "light", // Change to your desired topic
        qos: 0,
      },
      publish: {
        topic: "light", // Change to your desired topic
        qos: 0,
        payload: "", // This will be updated on button toggle
      },
      receiveNews: "",
      client: {
        connected: false,
        client: null, // This property will hold the actual MQTT client instance
      },
      subscribeSuccess: false,
      connecting: false,
      retryTimes: 0,
    };
  },
  created() {
    this.createConnection();
  },
  methods: {
    toggleButton() {
      this.buttonStatus = !this.buttonStatus;
      this.publish.payload = this.buttonStatus ? "ON" : "OFF";
      this.doPublish();
    },
    initData() {
      // ... (unchanged)
    },
    handleOnReConnect() {
      // ... (unchanged)
    },
    createConnection() {
      this.connecting = true;
      const { protocol, host, port, endpoint, ...options } = this.connection;
      const connectUrl = `${protocol}://${host}:${port}${endpoint}`;
      this.client.client = mqtt.connect(connectUrl, options);

      this.client.client.on("connect", () => {
        this.connecting = false;
        console.log("Connection succeeded!");
        this.doSubscribe();
      });

      this.client.client.on("reconnect", this.handleOnReConnect);
      this.client.client.on("error", (error) => {
        this.connecting = false;
        console.log("Connection failed", error);
      });
    
    },
    doSubscribe() {
      const { topic, qos } = this.subscription;
      this.client.client.subscribe(topic, { qos }, (error, granted) => {
        if (error) {
          console.log("Subscribe to topics error", error);
          return;
        }
        this.subscribeSuccess = true;
        console.log("Subscribe to topics granted", granted);
      });
    },
    doUnSubscribe() {
      // ... (unchanged)
    },
    doPublish() {
      const { topic, qos, payload } = this.publish;
      this.client.client.publish(topic, payload, { qos }, (error) => {
      console.log('topic',topic,'payload',payload);
        if (error) {
          console.log("Publish error", error);
        }
      });
    },
    destroyConnection() {
      if (this.client.connected) {
        try {
          this.client.client.end(false, () => {
            this.initData();
            console.log("Successfully disconnected!");
          });
        } catch (error) {
          console.log("Disconnect failed", error.toString());
        }
      }
    },
  },
};
</script>

<style scoped>
/* Add your component-specific styles here */
button {
  margin-bottom: 10px;
}
</style>

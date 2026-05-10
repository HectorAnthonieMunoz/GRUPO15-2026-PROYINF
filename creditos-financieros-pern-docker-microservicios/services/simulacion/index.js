
const express = require("express");
const cors = require("cors");
require("dotenv").config();
const { pool, connectWithRetry } = require("./db");
const simulacionRoutes = require("./routes/simulacionRoutes");
const recommendationRoutes = require("./routes/recommendation.routes")



const app = express();
app.use(cors());
app.use(express.json());

// Ruta de salud (health check)
app.get("/health", (req, res) => {
  res.status(200).json({ status: "OK", service: "simulacion" });
});

// Ruta de prueba
app.get("/", (req, res) => {
  res.send("Servicio Simulación funcionando 🚀");
});

// Rutas de simulación
app.use("/api", simulacionRoutes);

// ruta de recomendacion
app.use("/api", recommendationRoutes);

// Plantilla para agregar más rutas o middlewares
// app.use('/otra', require('./routes/otraRoutes'));

// Iniciar servidor con reintentos de conexión
const PORT = process.env.PORT || 3002;

async function startServer() {
  try {
    await connectWithRetry();
    app.listen(PORT, () => {
      console.log(`✅ Simulación escuchando en puerto ${PORT}`);
    });
  } catch (error) {
    console.error("❌ Error al iniciar el servidor:", error);
    process.exit(1);
  }
}

startServer();


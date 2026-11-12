# 📊 Plataforma Ejecutiva de Analítica Avanzada & Diagnóstico Financiero 360°
### *Business Intelligence, Machine Learning Supervisado & No Supervisado, Copiloto de Storytelling Dinámico y Síntesis Fonética por Voz (Voice AI)*

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://plataforma-ejecutiva-bi-storytelling-ml.streamlit.app/)
[![App En Vivo](https://img.shields.io/badge/Demo_En_Vivo-Visitar_Plataforma-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://plataforma-ejecutiva-bi-storytelling-ml.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Dashboards%20HD-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML%20Ensemble-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)
![Web Speech API](https://img.shields.io/badge/Voice%20AI-Web%20Speech%20API-10B981?style=for-the-badge&logo=soundcharts&logoColor=white)
![WCAG](https://img.shields.io/badge/Accessibility-WCAG%202.2%20AAA-0284C7?style=for-the-badge)

> ### 🌐 **Acceso Directo a la Aplicación en Vivo**
> Accede e interactúa en tiempo real con el dashboard, los modelos predictivos de Machine Learning y la locución fonética por voz en Streamlit Cloud:  
> 🔗 **[https://plataforma-ejecutiva-bi-storytelling-ml.streamlit.app/](https://plataforma-ejecutiva-bi-storytelling-ml.streamlit.app/)**

---

## 🧭 Visión General del Proyecto

La **Plataforma Ejecutiva de Analítica Avanzada & Diagnóstico Financiero** ([visitar demo interactiva](https://plataforma-ejecutiva-bi-storytelling-ml.streamlit.app/)) es un centro de comando integral de Business Intelligence y Ciencia de Datos diseñado para comités de dirección, directores de finanzas (CFO), operaciones (COO) y ventas (CRO).

Integra en una única experiencia interactiva:
1. **Modelado Financiero 360°**: Desglose P&L de facturación, costo directo (COGS), margen bruto retenido, inversión en adquisición (CAC total) y margen de contribución neta, junto con Unit Economics clave (`LTV/CAC`).
2. **Machine Learning Supervisado (Predictive Churn)**: Clasificación y discriminación probabilística de riesgo de abandono mediante ensemble de Random Forest, Gradient Boosting y Regresión Logística con validación cruzada estratificada (5-Fold CV) y curvas ROC.
3. **Machine Learning No Supervisado (Clustering RFM)**: Segmentación conductual multivariada mediante K-Means y análisis PCA con diagnóstico de K óptimo (Método del Codo y Coeficiente de Silueta).
4. **Copiloto de Storytelling Dinámico con Voz (Voice AI)**: Narraciones ejecutivas generadas en tiempo real que se adaptan a los filtros activos, acompañadas de sintetizadores de voz fonéticos en español basados en la **Web Speech API**, que leen tanto los diagnósticos de los gráficos como las conclusiones y tips operativos de cada tabla.
5. **Navegación Fija & Arquitectura Bento Grid**: Barra de navegación sticky con 11 pestañas temáticas, tarjetas KPI con animaciones de ola marina y esquemas cromáticos divergentes calibrados para accesibilidad y alto contraste.

---

## 🎛️ Las 11 Pestañas Analíticas

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 🧭 1. Resumen  │ 📈 2. Comercial │ 💰 3. Finanzas │ 🤖 4. Churn ML │ 🎯 5. RFM │ 🗺️ 6. Territorio │
│ 👥 7. Clientes │ 👔 8. Vendedores │ 📦 9. Catálogo │ 📐 10. Estadíst. │ 📋 11. Auditoría │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### 1. 🧭 Resumen Ejecutivo
* **Scorecard de Salud Global**: Semáforo estratégico de 8 indicadores vitales (Margen %, Contribución neta %, LTV/CAC, Churn, SLA logístico, CSAT).
* **Treemap Financiero**: Mapa de calor jerárquico de categorías y SKUs con escala semafórica según margen bruto.
* **Flujos Sankey & Heatmaps**: Mapeo del origen de ingresos desde el canal comercial hasta la línea de negocio y distribución regional.
* **Narrativa de Audio y Tips**: Diagnóstico automatizado con locución por voz y tips ejecutivos de rescate de facturación en riesgo.

### 2. 📈 Comercial & Tendencias
* **Evolución Temporal**: Ventas mensuales, media móvil trimestral (3m) y regresión lineal con pendiente de tendencia e índice $R^2$.
* **Descomposición Sunburst**: Flujo anular de Tipo de Cuenta → Canal de Venta.
* **Estacionalidad Cruzada**: Heatmap mensual por canal de venta.
* **Tabla de Rendimiento por Canal**: Ticket promedio, margen comercial, costo de adquisición (CAC) y ratio multiplicador Margen / CAC.

### 3. 💰 Finanzas 360° & Márgenes
* **Cascada Financiera (Waterfall)**: De Facturación Bruta → COGS → Margen Bruto → Inversión CAC → Contribución Neta final.
* **Sensibilidad de Descuentos**: Impacto de descuentos comerciales (0% al 20%) sobre el margen retenido.
* **Retorno sobre CAC**: Margen generado por cada $1 invertido en adquisición desglosado por segmento.
* **P&L por Línea de Negocio**: Estado de resultados consolidado por categoría comercial.

### 4. 🤖 Predictive Churn (Machine Learning) & What-If
* **Ensemble Supervisado**: Comparativa de Random Forest, Gradient Boosting y Regresión Logística con curvas ROC y matrices de confusión.
* **Importancia de Variables**: Identificación de los pesos relativos predictores del abandono (Recencia, CSAT, Frecuencia, Descuentos).
* **Simulador Interactivo What-If**: Sliders para evaluar en vivo la probabilidad estimada de churn de un cliente según días de inactividad, frecuencia, satisfacción y volumen de compra.
* **Top 15 Cuentas en Riesgo Crítico**: Tabla priorizada con cálculo exacto del capital expuesto y acciones recomendadas (Retención VIP, Contacto Inmediato, Monitoreo).

### 5. 🎯 Segmentación K-Means & RFM
* **Diagnóstico de Clústeres**: Curvas de Inercia (Codo) y Coeficiente de Silueta para seleccionar $K$ entre 2 y 6 grupos.
* **Reducción de Dimensionalidad PCA**: Mapeo bidimensional de los patrones de compra de los clientes.
* **Matriz RFM 5x5**: Heatmap de Recencia ($R$) vs Frecuencia ($F$) con volumen facturado.
* **Perfil Conductual y Estrategia**: Tabla de acciones comerciales diferenciadas por clúster (Élite VIP, Alto Potencial, Núcleo Recurrente, Enfriamiento, Dormidos).

### 6. 🗺️ Territorio & Operaciones Logísticas
* **Desempeño Regional**: Facturación y margen bruto por macro-regiones geográficas.
* **Cuellos de Botella Logísticos**: Heatmap de tasa de entregas demoradas por combinación de Región × Canal.
* **Impacto Logístico en CSAT**: Análisis del castigo en calificaciones de satisfacción ante entregas fuera del SLA.
* **Top 10 Plazas Comerciales**: Ranking de ciudades líderes en facturación.

### 7. 👥 Clientes Pareto 80/20 & Cartera ABC
* **Curva de Lorenz (Pareto)**: Verificación visual de concentración donde el 20% superior genera más del 70% de la facturación.
* **Distribución ABC**: Segmentación de cartera en Clase A (80%), Clase B (15%) y Clase C (5%).
* **Matriz Valor vs Riesgo**: Gráfico de dispersión cruzando volumen facturado, riesgo de deserción y LTV estimado.
* **Top 20 Cuentas Estratégicas**: Ranking con auditoría de recurrencia, margen y satisfacción.

### 8. 👔 Fuerza de Ventas 360°
* **Score Compuesto Ponderado**: Evaluación integral de asesores considerando 30% volumen, 25% margen retenido, 15% CSAT, 15% retención de cuentas y 15% disciplina en descuentos.
* **Cumplimiento de Metas**: Comparativa interactiva de ventas reales vs cuota asignada con slider de metas dinámico.
* **Eficiencia de Negociación**: Dispersión de descuento otorgado frente a margen logrado.

### 9. 📦 Portafolio & Matriz BCG
* **Cuadrantes de Portafolio**: Clasificación automática en SKUs Estrella, Volumen (Vaca lechera), Nicho Rentable y Revisar.
* **Treemap Jerárquico**: Desglose de ingresos y margen bruto ponderado por SKU.
* **Dispersión de Precios Unitarios**: Diagrama de cajas (box plot) en escala logarítmica por categoría.

### 10. 📐 Estadística Avanzada & Pruebas de Hipótesis
* **Matriz de Correlación No Paramétrica**: Coeficientes de correlación monótona de Spearman ($\rho$).
* **Distribución y Asimetría**: Histogramas con cajas marginales y cálculo de asimetría (*skewness*).
* **Pruebas de Hipótesis (95% Confianza)**:
  * Correlaciones de Spearman (Recencia $\leftrightarrow$ Churn, CSAT $\leftrightarrow$ Churn, Descuento $\leftrightarrow$ Margen).
  * Prueba de Kruskal-Wallis para varianza de margen entre líneas de negocio.
  * Prueba U de Mann-Whitney para comprobar el impacto del retraso en el CSAT.

### 11. 📋 Auditoría Operativa & Calidad de Datos
* **Explorador Transaccional Granular**: Filtros por búsqueda de texto, niveles de alerta y ordenamiento multi-criterio.
* **Descarga Multi-formato**: Exportación directa a CSV y Excel (`.xlsx`) enriquecido.
* **7 Controles Automáticos de Integridad**: Verificación en tiempo real de unicidad de ID, nulidad en campos críticos, consistencia contable (`Monto - Costo = Margen`), límites de porcentajes y escala CSAT.

---

## 📁 Estructura del Dataset (`dataset_analytics_storytelling_ml_500.xlsx`)

El conjunto de datos incluye 500 órdenes representativas de una empresa de tecnología y suministros corporativos:

| Variable | Tipo | Descripción |
|:---|:---:|:---|
| `Cliente_ID` | Numérico | Identificador único de transacción y cliente |
| `Nombre_Cuenta_Cliente` | Texto | Nombre de la razón social o cuenta corporativa |
| `Tipo_Cliente_Cuenta` | Categórico | B2B Corporativo, Consumidor Final, PYME / Prosumer |
| `Region` | Categórico | Metropolitana, Cibao / Norte, Este, Sur |
| `Ciudad` | Texto | Ciudad donde se registró la entrega o sucursal |
| `Canal_Venta` | Categórico | Ejecutivo B2B / Directo, E-Commerce, Showroom, WhatsApp |
| `Vendedor_Asignado` | Categórico | Asesor comercial a cargo de la cuenta |
| `Categoria` | Categórico | Infraestructura & Servidores, Gaming & Alto Rendimiento, etc. |
| `Producto_Principal` | Texto | SKU insignia adquirido en la transacción |
| `Fecha_Transaccion` | Fecha | Timestamp de la compra (rango 2025–2026) |
| `Cantidad_Productos` | Entero | Volumen físico de unidades en la orden |
| `Monto_Compra` | Moneda ($) | Facturación bruta de la orden |
| `Costo_Total` | Moneda ($) | Costo directo de mercancías vendidas (COGS) |
| `Margen_Bruto` | Moneda ($) | Utilidad bruta (`Monto_Compra - Costo_Total`) |
| `Margen_Bruto_Pct` | Porcentaje | Margen porcentual (`Margen / Monto * 100`) |
| `Descuento_Pct` | Porcentaje | Descuento comercial aplicado a la orden |
| `CAC_Estimado` | Moneda ($) | Costo de adquisición de cliente imputado |
| `LTV_Estimado_USD` | Moneda ($) | Valor de vida proyectado de la cuenta |
| `Satisfaccion_CSAT` | Escala 1-5 | Calificación de satisfacción del cliente |
| `SLA_Entrega_Dias` | Entero | Tiempo de entrega en días hábiles |
| `Estado_Entrega` | Categórico | "Entregado a Tiempo" / "Con Retraso Logístico" |
| `Recencia_Dias` | Entero | Días transcurridos desde la última compra |
| `Frecuencia_Historica`| Entero | Número de transacciones acumuladas por la cuenta |
| `Riesgo_Churn_Score` | Probabilidad | Score numérico de propensión de fuga (0.00 a 1.00) |
| `Alerta_Riesgo_Churn` | Categórico | "Cliente Fiel / Estable", "Monitoreo / Medio", "Alto Riesgo" |

---

## 🚀 Instalación y Ejecución Local

### Prerrequisitos
* Python 3.10 o superior instalado.
* Git instalado.

### 1. Clonar el repositorio
```bash
git clone https://github.com/JUANCITOPENA/Plataforma-Ejecutiva-BI-Storytelling-ML.git
cd Plataforma-Ejecutiva-BI-Storytelling-ML
```

### 2. Crear y activar entorno virtual (Recomendado)
```bash
# En Windows (PowerShell):
python -m venv env
.\env\Scripts\Activate.ps1

# En Linux / macOS:
python3 -m venv env
source env/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Iniciar la aplicación
```bash
streamlit run app.py
```
La plataforma se abrirá automáticamente en tu navegador predeterminado en `http://localhost:8501`.

---

## ☁️ Publicación en Streamlit Community Cloud

Esta plataforma se encuentra desplegada y operativa en producción en **Streamlit Community Cloud**:

🔗 **Enlace Oficial**: [https://plataforma-ejecutiva-bi-storytelling-ml.streamlit.app/](https://plataforma-ejecutiva-bi-storytelling-ml.streamlit.app/)

### Parámetros de Configuración en la Nube:
* **Repository**: `JUANCITOPENA/Plataforma-Ejecutiva-BI-Storytelling-ML`
* **Branch**: `main`
* **Main file path**: `app.py`
* **App URL**: `https://plataforma-ejecutiva-bi-storytelling-ml.streamlit.app/`
* **Requisitos**: Instalados automáticamente vía `requirements.txt`.

---

## 🛠️ Stack Tecnológico & Arquitectura

* **Frontend & Dashboarding**: [Streamlit](https://streamlit.io/) v1.35+ con inyección de componentes HTML5 / CSS3 Bento Grid y Web Speech API.
* **Manipulación de Datos**: [Pandas](https://pandas.pydata.org/) 2.2+ y [NumPy](https://numpy.org/) 1.26+.
* **Visualizaciones Interactivas**: [Plotly Express & Graph Objects](https://plotly.com/python/) con tooltips HD estilizados y paletas financieras WCAG AAA.
* **Machine Learning**: [Scikit-Learn](https://scikit-learn.org/) (RandomForest, GradientBoosting, LogisticRegression, KMeans, PCA, StandardScaler, StratifiedKFold).
* **Estadística Inferencial**: [SciPy](https://scipy.org/) (Spearman, Kruskal-Wallis, Mann-Whitney U).
* **Gestión de Hojas de Cálculo**: [OpenPyXL](https://openpyxl.readthedocs.io/).

---

## 👤 Autor & Créditos

**Ing. Juancito Peña Vizcaíno**  
*Arquitecto de Soluciones de Datos, Analítica Avanzada & Inteligencia Artificial*  
* Santo Domingo, República Dominicana  
* Canal Educativo: [@JuancitoDevV](https://www.youtube.com/@JuancitoDevV)  
* GitHub: [JUANCITOPENA](https://github.com/JUANCITOPENA)

---

### 📄 Licencia
Este proyecto se distribuye bajo la licencia **MIT**. Consulta el archivo `LICENSE` para más información.

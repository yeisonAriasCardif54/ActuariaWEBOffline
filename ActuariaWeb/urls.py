"""ActuariaWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

# -- IMPORTAMOS VISTAS DEL MODULO DESK -- #
from desk.views_ import inicio

# -- IMPORTAMOS VISTAS DEL MODULO PROFITABILITY -- #
from profitability.views_ import views_pgv
from profitability.views_ import views_pgv_creadores_vs_destructores
from profitability.views_ import views_reporte2
from profitability.views_ import views_herramienta_presupuesto
from profitability.views_ import views_herramienta_presupuesto_historico
from profitability.views_ import views_herramienta_presupuesto_resumen
from profitability.views_ import views_calcular_rrc
from profitability.views_ import views_herramienta_optimizacion

# -- IMPORTAMOS VISTAS DEL MODULO PRICING -- #
from pricing.views_ import views_table_update
# -- ACQUISITION COSTS
from pricing.views_ import acquisition_cost
# -- WPT - BP
from pricing.views_ import WPT_BP
# -- Technical Analysis Note - Templates
from pricing.views_ import tan
# -- WPT - Tarificador
from pricing.views_ import tarificador
from pricing.views_ import tarificador_administrador
from pricing.views_ import tarificador_tags

# -- IMPORTAMOS VISTAS DEL MODULO EXPOST -- #
from expost.views_ import frecuencia
from expost.views_ import frecuencia_qx
from expost.views_ import rt_ocurr_q
from expost.views_ import rt_incu
from expost.views_ import persist_km
from expost.views_ import persist_triang
from expost.views_ import data_expost
from expost.views_ import life_eg

# -- VISTAS DEL MODULO RECURSOS
from recursos.views_ import implementacion
from recursos.views_ import superintendencia

# -- CONFIGURACIÓN DEL ADMIN -- #
admin.site.site_header = 'Panel de administración Actuaría Web'
admin.site.site_title = 'Panel de administración Actuaría Web'

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),

                  # ---- Home ---- #
                  path('', inicio.inicio, name="Inicio"),

                  # ---- profitability - pgv ---- #
                  path('pgv', views_pgv.reporte1, name="Reporte PGV"),
                  path('pgv_graficar', views_pgv.pgv_graficar, name="pgv_graficar"),

                  # ---- profitability - creadores vs destructores ---- #
                  path('pgv2', views_pgv_creadores_vs_destructores.reporte, name="Reporte PGV"),
                  path('pgv2_graficar', views_pgv_creadores_vs_destructores.pgv_graficar, name="pgv_graficar"),

                  # ---- profitability - reporte2 y 3 ---- #
                  path('reporte2', views_reporte2.reporte2, name="Reporte 2"),
                  path('reporte3', views_reporte2.reporte3, name="Reporte 3"),
                  path('reporte4', views_reporte2.reporte4, name="Reporte 4"),

                  # ---- profitability - Herramienta de presupuesto ---- #
                  path('herramienta_presupuesto', views_herramienta_presupuesto.index, name="Presupuesto"),
                  path('herramienta_presupuesto/generate', views_herramienta_presupuesto.generate, name="Presupuesto"),
                  path('herramienta_presupuesto/generateFavorites', views_herramienta_presupuesto.generateFavorites, name="Presupuesto"),
                  path('herramienta_presupuesto/get_history', views_herramienta_presupuesto.get_history, name="Presupuesto"),
                  path('herramienta_presupuesto/get_history_group', views_herramienta_presupuesto.get_history_group, name="Presupuesto"),
                  path('herramienta_presupuesto/history_favorite', views_herramienta_presupuesto.history_favorite, name="Presupuesto"),
                  path('herramienta_presupuesto/update_state', views_herramienta_presupuesto.update_state, name="Presupuesto"),
                  path('herramienta_presupuesto/convert_xlsx', views_herramienta_presupuesto.convert_xlsx, name="Presupuesto"),

                  # ---- profitability - Herramienta de optimización del presupuesto ---- #
                  path('herramienta_optimizacion', views_herramienta_optimizacion.index, name="OptimizacionPresupuesto"),
                  path('herramienta_optimizacion/generate', views_herramienta_optimizacion.generate, name="OptimizacionPresupuesto"),

                  # ---- profitability - Herramienta de presupuesto - Histórico ---- #
                  path('herramienta_presupuestoH/historico', views_herramienta_presupuesto_historico.view_history, name="Presupuesto Histórico"),
                  path('herramienta_presupuestoH/get_history_all', views_herramienta_presupuesto_historico.get_history_all, name="Presupuesto Histórico"),

                  # ---- profitability - Herramienta de presupuesto - Resumen ---- #
                  path('herramienta_presupuestoR/resumen', views_herramienta_presupuesto_resumen.index, name="Presupuesto Resumen"),

                  # ---- profitability - Herramienta para calcular DesembolsosSt y RRC ---- #
                  path('calcular_rrc', views_calcular_rrc.index, name="Presupuesto - Calcular DesembolsosSt y RRC"),
                  path('calcular_rrc/generate', views_calcular_rrc.generate, name="Presupuesto - Calcular DesembolsosSt y RRC"),

                  # ---- pricing - Actualizar tabla pricing ---- #
                  path('table', views_table_update.index, name="Pricing - Actualizar tabla"),
                  path('table_ajax', views_table_update.get_table_ajax, name="Pricing Ajax"),

                  # ---- pricing - ACQUISITION_COSTS ---- #
                  path('acquisition_cost', acquisition_cost.index, name="Pricing - acquisition_cost"),
                  path('acquisition_cost_ajax', acquisition_cost.get_ajax, name="Pricing acquisition_cost Ajax"),
                  path('acquisition_cost/update', acquisition_cost.update, name="Pricing acquisition_cost Update"),

                  # ---- pricing - Technical Analysis Note - Templates ---- #
                  path('tan', tan.index, name="Pricing - Technical Analysis Notes"),
                  path('tan/generate', tan.generate, name="Pricing - Technical Analysis Notes - Generate"),

                  # ---- pricing - WPT - BP ---- #
                  path('business_plan_tool', WPT_BP.index, name="Business Plan"),
                  path('business_plan_tool/generate', WPT_BP.generate, name="WPT - Calcular Business Plan"),
                  path('business_plan_tool/history', WPT_BP.history, name="WPT - Histórico Business Plan"),
                  path('business_plan_tool/historyTable/<int:category>', WPT_BP.historyTable, name="WPT - Histórico Business Plan - Tabla"),
                  path('business_plan_tool/change_category', WPT_BP.change_category, name="WPT - Histórico Business Plan - cambiar categoría"),
                  path('business_plan_tool/update_state', WPT_BP.update_state, name="WPT - Histórico Business Plan - eliminar BP"),
                  path('business_plan_tool/generate_from_tarificador/<int:idTarificador>', WPT_BP.generate_from_tarificador, name="WPT - Calcular Business Plan - Desde archivo tarificador"),

                  # ---- pricing - Tarificador ---- #
                  path('tarificador', tarificador.index, name="Upload tarificador"),
                  path('tarificador/preUpload', tarificador.preUpload, name="PRE Upload tarificador Ajax"),
                  path('tarificador/upload', tarificador.upload, name="Upload tarificador Ajax"),
                  path('tarificador/administrador', tarificador_administrador.index, name="Administrador de tarificadores"),
                  path('tarificador/tableAjax/<int:category>', tarificador_administrador.table, name="Administrador de tarificadores - Tabla Ajax"),
                  path('tarificador/change_tag', tarificador_administrador.change_tag, name="WPT - Histórico Business Plan - cambiar categoría"),
                  path('tarificador/update_state', tarificador_administrador.update_state, name="WPT - Histórico Business Plan - eliminar BP"),
                  path('tarificador/tagsAdd', tarificador_tags.add, name="Administrar tags"),
                  path('tarificador/tagsSave', tarificador_tags.save, name="Administrar tags - Agregar"),
                  path('tarificador/tagsEdit/<int:tag>', tarificador_tags.edit, name="Administrar tags - Editar"),
                  path('tarificador/tagsUpdate/<int:tag>', tarificador_tags.update, name="Administrar tags - Editar"),

                  # ---- expost - Dash Vigentes ---- #
                  path('frecuencia', frecuencia.index, name="Frecuencia"),
                  path('frecuencia_selects', frecuencia.selects, name="Obtener listas desplegables"),
                  path('frecuencia_qx', frecuencia_qx.index, name="Frecuencia_qx"),
                  path('frecuencia_qx_selects', frecuencia_qx.selects, name="Obtener listas desplegables"),
                  path('rt_ocurr_q', rt_ocurr_q.index, name="RT_OCURR_Q"),
                  path('rt_ocurr_q_selects', rt_ocurr_q.selects, name="RT_OCURR_Q desplegables"),
                  path('rt_incu', rt_incu.index, name="RT_INCU"),
                  path('rt_incu_selects', rt_incu.selects, name="Obtener listas desplegables"),
                  path('data_expost', data_expost.index, name="DATA"),
                  path('data_expost_export_expu', data_expost.export_expu, name='export_expu'),
                  path('data_expost_export_vige', data_expost.export_vige, name='export_vige'),
                  path('data_expost_export_rrc', data_expost.export_rrc, name='export_rrc'),
                  path('data_expost_export_nuevos', data_expost.export_nuevos, name='export_nuevos'),
                  path('persist_km', persist_km.index, name="K_M"),
                  path('persist_km_selects', persist_km.selects, name="Obtener listas desplegables"),
                  path('persist_triang', persist_triang.index, name="TRIANGULOS"),
                  path('persist_triang_selects', persist_triang.selects, name="Obtener listas desplegables"),
                  path('life_eg', life_eg.index, name="life_eg"),
                  path('life_eg_selects', life_eg.selects, name="life_eg_despleg"),

                  # ---- RECURSOS ---- #
                  path('recursos/implementacion-tan', implementacion.tan, name="Administrador de tarificadores"),
                  path('recursos/tableAjax/<int:category>', implementacion.table, name="Administrador de tarificadores - Tabla Ajax"),
                  path('recursos/formato/<int:id>', implementacion.formato, name="Administrador de tarificadores - Formato implementacion"),

                  # ---- RECURSOS INFORMES SUPERINTENDENCIA ---- #
                  path('recursos/ISF-dashboard', superintendencia.dashboard, name="Superintendencia - Dashboard"),
                  path('recursos/ISF-dashboard-graficar', superintendencia.dashboard_graficar, name="Dashboard Gráfica"),
                  path('recursos/ISF-historico', superintendencia.historico, name="Superintendencia - Histórico"),
                  path('recursos/ISF-historico_graficar', superintendencia.historico_graficar, name="Histórico Gráfica"),
                  path('recursos/ISF-simulador', superintendencia.simulador, name="Superintendencia - Simulador"),
                  path('recursos/ISF-simulador_graficar', superintendencia.simulador_graficar, name="Simulador Gráfica"),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

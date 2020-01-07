Public Sub HerramientaPpto() 'Genera el presupuesto comùn y corriente

tinicio = DateTime.Now 'Temporizador
Application.ScreenUpdating = False 'No actualizar paginas

'Verificar que no haya filtros en las paginas
Sheets("ParametrosSt").Activate
If ActiveSheet.FilterMode Then ActiveSheet.ShowAllData 'Quitar todos los filtros
Sheets("DesembolsosSt").Activate
If ActiveSheet.FilterMode Then ActiveSheet.ShowAllData 'Quitar todos los filtros
Sheets("ParametrosNv").Activate
If ActiveSheet.FilterMode Then ActiveSheet.ShowAllData 'Quitar todos los filtros
Sheets("DesembolsosNv").Activate
If ActiveSheet.FilterMode Then ActiveSheet.ShowAllData 'Quitar todos los filtros
Sheets("RRC").Activate
If ActiveSheet.FilterMode Then ActiveSheet.ShowAllData 'Quitar todos los filtros
Sheets("Consola").Activate 'Voler a la pagina inicial


'Verificación de base real incluida------------------------------------------
If Sheets("Consola").Cells(13, 3) = "Si" And Sheets("BaseReal").Cells(2, 3) <= 0 Then
   MsgBox ("Debe ingresar una base real que se pueda imprimir")
   GoTo 10000
End If

'Lectura de parametros generales:--------------------------------------------
finanp = Sheets("Consola").Cells(5, 3) 'Tasa de costo de oportunidad
meses = Sheets("Consola").Cells(6, 3) 'Meses a proyectar
mesiniciost = Sheets("Consola").Cells(7, 3)
mesinicio = Sheets("Consola").Cells(9, 3) 'Mes de arranque de proyeciòn
mesesimprime = Sheets("Fechas").Range("G1").End(xlDown).Row - 1 'Meses maximo a imprimir. Se espera que sean 121 (10 años+mes cero)
mesanual = Sheets("Consola").Cells(6, 7) 'Meses transcurridos desde enero del año de la proyección
ipc = Sheets("Consola").Cells(10, 3) 'Ipc del año
caidaren = Sheets("Consola").Cells(11, 3) 'Caida general de las renovaciones
msipc = Sheets("Consola").Cells(12, 3) 'Supuesto de meses que tienen en promedio los clientes del stock mensual
piva = Sheets("Consola").Cells(8, 3) '% de IVA
pica = Sheets("Consola").Cells(14, 3) '% de ICA
pgmf = Sheets("Consola").Cells(15, 3) '% de GMF
taxr = Sheets("Consola").Cells(16, 3) 'Tasa de impuesto
tipincent = Sheets("Consola").Cells(7, 7) 'Tipo de pago de incentivos

'Determinar no. productos stock
If IsEmpty(Sheets("ParametrosSt").Range("A2")) = False Then 'Si no està vacia realice el conteo
   sproduct = Sheets("ParametrosSt").Range("A1").End(xlDown).Row - 1 'Numero de productos en stock
Else 'De lo contrario es cero
   sproduct = 0
End If

If IsEmpty(Sheets("ParametrosNv").Range("A2")) = False Then 'Si no està vacia realice el conteo
   nproduct = Sheets("ParametrosNv").Range("A1").End(xlDown).Row - 1 'Productos nuevos
Else 'De lo contrario es cero
   nproduct = 0
End If

totalproduct = sproduct + nproduct 'Totaliza el número de productos de stock y nuevos
nparametros = Sheets("ParametrosSt").Range("A1").End(xlToRight).Column - 6 'Numero de parametros
ngrupos = Sheets("Consola").Range("T1").End(xlDown).Row - 1 'Numero de grupos
nstocks = Sheets("RRC").Range("A1").End(xlDown).Row - 1 'Numero de productos que tendrán stocks de RRC
nsocios = Sheets("Consola").Range("K1").End(xlDown).Row - 1 'Numero de socios
nofertas = Sheets("Consola").Range("N1").End(xlDown).Row - 1 'Numero de ofertas
ntipos = Sheets("Consola").Range("Q1").End(xlDown).Row - 1 'Numero de tipos
ngrupos = Sheets("Consola").Range("T1").End(xlDown).Row - 1 'Numero de grupos de PU


'Determina los arrays para luego cambiar id's por nombres:
ReDim infsocio(1 To nsocios) 'Guarda el id de todos los socios
For i = 1 To nsocios
   infsocio(i) = Cells(i + 1, 12)
Next i

ReDim infoferta(1 To nofertas) 'Guarda el id de todas las ofertas
For i = 1 To nofertas
  infoferta(i) = Cells(i + 1, 15)
Next i

ReDim inftipoprima(1 To ntipos) 'Guarda el id de todos los tipos de prima
For i = 1 To ntipos
  inftipoprima(i) = Cells(i + 1, 18)
Next i

ReDim fechas(0 To mesesimprime) 'Guarda las fechas según un ID
For i = 0 To mesesimprime
  fechas(Sheets("Fechas").Cells(i + 2 + mesanual, 7)) = Sheets("Fechas").Cells(i + 2 + mesanual, 8)
Next i

ReDim infgrupopu(1 To ngrupos, 1 To 6) 'Guarda el id de todos los grupos de PU
For i = 1 To ngrupos
  infgrupopu(i, 1) = Cells(i + 1, 20) 'Tomará el ID
  infgrupopu(i, 2) = Cells(i + 1, 22) 'Tomará el % de costo de capital del grupo i
  infgrupopu(i, 3) = Cells(i + 1, 23) 'Tomará el % de participación de utilidad
  infgrupopu(i, 4) = Cells(i + 1, 21) 'Nombre del grupo
  infgrupopu(i, 5) = Cells(i + 1, 24) 'Pagado acumulado del grupo
  infgrupopu(i, 6) = Cells(i + 1, 25) 'Profit acumulado del grupo
Next i

'Vector del manejo de RRC
ReDim vector(1 To 5)
For i = 1 To 5
  vector(i) = Cells(i + 9, 6) 'Tomará el ID
Next i

'Determinar arreglo de los prodcutos:
ReDim infproducto(1 To nparametros + 1, 0 To meses) 'se sum+1 porque falta la dimensión del desembolso
Dim Mesgarantia As Integer
Dim tcutoff As Integer
ReDim particomin(1 To 2) 'Participacion de las comisiones: 1 para socio, 2 para broker
ReDim pugroup(1 To totalproduct) 'Grupos de PU
ReDim amortiz(1 To totalproduct) 'Meses de amortizacion


'Determinar dimension de la lista de conceptos del P&G:
ReDim nuevos(1 To meses + mesiniciost) 'Clientes nuevo
ReDim vig(0 To meses, 1 To meses) 'vigentes del producto i, en el mes k, de la cosecha t
ReDim vigentes(0 To meses + mesiniciost) 'vigentes del producto i, en el mes k (considera todas las cosechas)
ReDim vigentes1(1 To meses + mesiniciost) 'Corresponde a los vigentes del producto i stock, en el mes k. considera todas las cosechas de las renovaciones
ReDim vigentestock(0 To meses) 'Hace referencia a los vigentes que entran como input al modelo
ReDim dacstock(0 To meses)
ReDim penetracion(1 To meses) 'indica la penetración del producto i en el mes k, solo será para productos nuevos
ReDim cancel(0 To meses, 1 To meses)  'Cancelaciònes del producto i, de la campaña t, en el mes k
ReDim cancela(1 To meses + mesiniciost) 'Cancelaciònes del producto i, en el mes k. Agrupa por cosechas
ReDim sinies(1 To meses + mesiniciost) 'Siniestros del producto i en el mes k
ReDim gwp(1 To meses + mesiniciost)
ReDim gwpn(1 To meses)
ReDim gwpnt(1 To meses, 1 To meses)
ReDim gwps(1 To meses)
ReDim gwpst(1 To meses, 1 To meses)
ReDim vlrprimac(0 To meses, 0 To meses)
ReDim vlrprimad(0 To meses, 0 To meses)
ReDim upr(0 To meses + mesiniciost) 'Reserva del producto i, en el tiempo k
ReDim upr1(1 To meses + mesiniciost) 'Reserva del producto i, en el tiempo k, de todas las renovaciones
ReDim uprt(1 To meses, 1 To meses + mesiniciost) 'Reserva para cada una de las cosechas t, en el tiempo k
ReDim uprstock(0 To meses) 'Reserva del producto i, en el tiempo k en curso
ReDim earnedP(1 To totalproduct, 1 To meses + mesiniciost) 'Prima devengada
ReDim commin(1 To meses + mesiniciost) 'Comisiones
ReDim dac(1 To meses + mesiniciost)
ReDim dac1(1 To meses) 'Hace referencia a las comisiones reservadas de las renovaciones
ReDim earnedC(1 To totalproduct, 1 To meses + mesiniciost)
ReDim incurC(1 To totalproduct, 1 To meses + mesiniciost)
ReDim ResulTec(1 To totalproduct, 1 To meses)
ReDim vatp(1 To meses + mesiniciost) 'VAT pagado
ReDim vata(1 To meses + mesiniciost) 'VAT amotizado
ReDim incentp(1 To meses + mesiniciost) 'Costo de incentivo Pagado One Shot
ReDim incent(1 To meses + mesiniciost) 'Costo de incentivos
ReDim tmkCost(1 To meses + mesiniciost) 'Costos de TMKT
ReDim vatincent(1 To meses + mesiniciost) 'VAT pagado
ReDim vatmk(1 To meses + mesiniciost) 'VAT pagado

'Arreglos para agrupar todos los resultados por mes
ReDim gross1(1 To meses)
ReDim gross2(1 To totalproduct, 1 To meses)
ReDim capitalcost1(1 To meses) 'EP - EC
ReDim pu(1 To meses)
ReDim pu2(1 To meses)
ReDim pureal(1 To totalproduct, 1 To meses)
ReDim puincur(1 To totalproduct, 1 To meses) 'PU incurrida
ReDim acumpu(0 To meses) 'es como el acumprofit
ReDim ica(1 To meses + mesiniciost) 'Impuesto del ICA
ReDim gmf(1 To meses + mesiniciost) '4x1000
ReDim gastos(1 To totalproduct, 1 To meses + mesiniciost)

'Variables para el agrupamiento por Grupo
ReDim nuevosg(1 To meses + mesiniciost, 1 To ngrupos) 'Clientes nuevos del grupo i
ReDim vigenteg(1 To meses + mesiniciost, 1 To ngrupos)
ReDim cancelag(1 To meses + mesiniciost, 1 To ngrupos)
ReDim siniestrog(1 To meses + mesiniciost, 1 To ngrupos)
ReDim GWPg(1 To meses + mesiniciost, 1 To ngrupos)
ReDim UPRg(1 To meses + mesiniciost, 1 To ngrupos)
ReDim earnedPreg(1 To meses + mesiniciost, 1 To ngrupos)
ReDim coming(1 To meses + mesiniciost, 1 To ngrupos)
ReDim DACg(1 To meses + mesiniciost, 1 To ngrupos)
ReDim earnedCog(1 To meses + mesiniciost, 1 To ngrupos)
ReDim incurCg(1 To meses + mesiniciost, 1 To ngrupos)
ReDim resulTecg(1 To meses + mesiniciost, 1 To ngrupos)
ReDim VAT_Paidg(1 To meses + mesiniciost, 1 To ngrupos)
ReDim VAT_Amortig(1 To meses + mesiniciost, 1 To ngrupos)
ReDim incentig(1 To meses + mesiniciost, 1 To ngrupos)
ReDim tmktCostg(1 To meses + mesiniciost, 1 To ngrupos)
ReDim vatincentg(1 To meses + mesiniciost, 1 To ngrupos)
ReDim vatmkg(1 To meses + mesiniciost, 1 To ngrupos)
ReDim goi1(1 To meses + mesiniciost, 1 To ngrupos) 'Primer goi para determinar si paga o no utilidades
ReDim goi2(1 To meses + mesiniciost, 1 To ngrupos) 'Segundo goi para calcular el resultado técnico
ReDim profit1g(1 To meses + mesiniciost, 1 To ngrupos) 'goi - costo de capital
ReDim profit2g(1 To meses + mesiniciost, 1 To ngrupos) 'goi - costo de capital
ReDim capitalcost(1 To meses + mesiniciost, 1 To ngrupos) 'EP - EC
ReDim overheadg(1 To meses + mesiniciost, 1 To ngrupos) 'Overheadas del grupo
ReDim acumprofitg(0 To meses + mesiniciost, 1 To ngrupos)
ReDim acumpurealg(0 To meses + mesiniciost, 1 To ngrupos)
ReDim purealg(1 To meses + mesiniciost, 1 To ngrupos)
ReDim puincurg(1 To meses + mesiniciost, 1 To ngrupos)
ReDim ResulTecAcum(1 To meses + mesiniciost, 1 To ngrupos)
ReDim icag(1 To meses + mesiniciost, 1 To ngrupos) 'Impuesto del ICA grupal
ReDim gmfg(1 To meses + mesiniciost, 1 To ngrupos) '4x1000 grupal

'Arreglos necesario para el calculo de los requerimiento de capital e ingreso financiero
ReDim fincomec(0 To meses) 'Ingresos financieros por capital, cada mes
ReDim fincomer(0 To meses) 'Ingresos financieros por reservas, cada mes
ReDim afincome(0 To meses) 'Ingresos financieros totales agrupados por año
Dim suminC As Double 'Suma de incurred claims para determinar los ingresos financieros
Dim sumGwp As Double  'Suma de GWP para determinar los ingresos financieros
ReDim reqcap(0 To meses) 'Requerimiento de capital por mes
ReDim reqcapy(0 To meses) 'Requerimiento de capital por año

'Para el calculo de los impuestos
ReDim tax(0 To meses)
ReDim Acumtax(0 To meses)
ReDim taxreal(1 To totalproduct, 0 To meses)
ReDim taxrealm(0 To meses)
ReDim Acumtaxrealm(0 To meses)
ReDim Acumgross2(0 To meses)
ReDim gross2m(0 To meses)


'********************* Aca empieza el procedimiento: ***************************************************************************
'Esqueleto del presupuesto: determinar los volumenes de nuevos, vigentes, siniestros, cancelados y valores de prima no devengada

ji = 0 'Contador del número de filas
k1 = mesinicio 'Cantidad de meses que han pasado desde el mes cero

For i = 1 To totalproduct

If i <= sproduct Then
'Recorrido para leer los parametros del stock:
Sheets("ParametrosSt").Activate
  For j = 1 To nparametros
    infproducto(j, 1) = Cells(i + 1, j)
  Next j
    Mesgarantia = Cells(i + 1, j)
    tcutoff = Cells(i + 1, j + 1)
    particomin(1) = Cells(i + 1, j + 2)
    particomin(2) = Cells(i + 1, j + 3)
    pugroup(i) = Cells(i + 1, j + 4)


'Recorrido para leer la proyección del desembolso:
Sheets("DesembolsosSt").Activate 'Todos los desembolsos del stock no son mas que las renovaciones proyectadas. Por esta razòn la penetraciòn siempre serà 100%
  For k = 0 To WorksheetFunction.Min(meses, 72) 'Sòlo hasta 72 meses porque se espera que despues de ese tiempo no haya renovaciones viejas
  infproducto(36, k) = Cells(i + 1, k + 2)
  Next k

Else
'Recorrido para leer los parametros de prodcutos nuevos en stock:
Sheets("ParametrosNv").Activate

  For j = 1 To nparametros
    infproducto(j, 1) = Cells(i + 1 - sproduct, j)
  Next j
    Mesgarantia = Cells(i + 1 - sproduct, j)
    tcutoff = Cells(i + 1 - sproduct, j + 1)
    particomin(1) = Cells(i + 1 - sproduct, j + 2)
    particomin(2) = Cells(i + 1 - sproduct, j + 3)
    pugroup(i) = Cells(i + 1 - sproduct, j + 4)
    amortiz(i) = Cells(i + 1 - sproduct, j + 5)
    j = 1

'Recorrido para leer la proyección del desembolso de los nuevos:
Sheets("DesembolsosNv").Activate
  For k = 0 To meses
      If k <= mesiniciost Then 'Si es antes del mes inicio de stock, no deben haber emisiones
         infproducto(36, k) = 0
      Else
         infproducto(36, k) = Sheets("DesembolsosNv").Cells(i + 1 - sproduct, k + 2)
      End If
  Next k
k = 1

End If

'*****************************************************************************************************

  If infproducto(19, 1) = "Nuevo" Or infproducto(19, 1) = "Stock" Then

    If infproducto(5, 1) = 3 Then 'Si la prima es única-----------------------------------------------

       For t = 1 To meses
       yvlrp = (t Mod 12)
           For k = t To meses
           If t = 1 Then
             vlrprimac(k, t) = infproducto(6, 1) * ((infproducto(4, 1) - k) / infproducto(4, 1))
             vlrprimad(k, t) = infproducto(6, 1) * ((infproducto(4, 1) - k + 0.5) / infproducto(4, 1))

           ElseIf t > 1 And yvlrp = 1 Then
             If infproducto(34, 1) = "Si" Then
               vlrprimac(k, t) = vlrprimac(k - 1, t - 1) * (1 + ipc)
               vlrprimad(k, t) = vlrprimad(k - 1, t - 1) * (1 + ipc)
             Else
               vlrprimac(k, t) = vlrprimac(k - 1, t - 1)
               vlrprimad(k, t) = vlrprimad(k - 1, t - 1)
             End If

           Else
             vlrprimac(k, t) = vlrprimac(k - 1, t - 1)
             vlrprimad(k, t) = vlrprimad(k - 1, t - 1)
           End If

          Next k
       Next t


     ElseIf infproducto(5, 1) = 2 Then 'Si la prima es Anual-------------------------------------------

       'Creación de los valores de prima para el primer año:
        For t = 1 To meses

              For k = t To 12

              If t = 1 Then
                  vlrprimac(k, t) = infproducto(6, 1) * ((12 - k) / 12)
                  vlrprimad(k, t) = infproducto(6, 1) * ((12 - k + 0.5) / 12)
              Else

                  vlrprimac(k, t) = vlrprimac(k - 1, t - 1)
                  vlrprimad(k, t) = vlrprimad(k - 1, t - 1)

              End If


             Next k
        Next t

     ElseIf infproducto(5, 1) = 4 Or infproducto(5, 1) = 5 Then 'Si la prima es Amortizada o multiprima-----------------------------------------------

       If amortiz(i) = "Natural" Then 'Agarra el error si encuentra un producto mal clasificado:
           MsgBox ("Hay un error clasificando un producto en amortizacion o  multiprima")
           GoTo 10000 'Saltar al final del procedimiento
         Else

            'Creación de los valores de prima para el primer año:
            For t = 1 To meses

                  For k = t To WorksheetFunction.Min(meses, amortiz(i))

                  If t = 1 Then
                      vlrprimac(k, t) = (infproducto(6, 1)) * amortiz(i) * ((amortiz(i) - k) / amortiz(i))
                      vlrprimad(k, t) = (infproducto(6, 1)) * amortiz(i) * ((amortiz(i) - k + 0.5) / amortiz(i))
                  Else

                      vlrprimac(k, t) = vlrprimac(k - 1, t - 1)
                      vlrprimad(k, t) = vlrprimad(k - 1, t - 1)

                  End If


                 Next k
            Next t
       End If

     Else 'Si la prima resulta ser mensual no haga nada porque no la prima por devenga toda el mismo mes

    End If

  Else 'Si es stock RRC, no recalcule las primas

  End If

'****************************************************************************************************************************************************************************************************************
'Si la prima resulta Nuevo
'****************************************************************************************************************************************************************************************************************
If infproducto(19, 1) = "Nuevo" Then

   For k = 1 To meses 'Primer recorrido para generar penetración porque esta si debe ir hasta meses, en cambio el recorrido de productos debe ir hasta meses-mesiniciost
     'Condición para el cutoff
     If k >= tcutoff And tcutoff > 0 Then
        penetracion(k) = 0

     Else

         'Condiciòn para determinar si la penetraciòn debe ser cero
         If k < infproducto(7, 1) Then

            penetracion(k) = 0
         Else
                'Generación de la penetración necesaria para producir los clientes nuevos
                If k <= (12 + infproducto(7, 1) - mesanual) Then  'Condición para determinar si ya paso el primer año

                   If (k + mesanual) <= 3 + infproducto(7, 1) Then 'Pregunta si está en el Q1
                      penetracion(k) = infproducto(20, 1)
                   ElseIf (k + mesanual) <= 6 + infproducto(7, 1) Then 'Pregunta si está en el Q2
                      penetracion(k) = infproducto(21, 1)
                   ElseIf (k + mesanual) <= 9 + infproducto(7, 1) Then 'Pregunta si está en el Q3
                      penetracion(k) = infproducto(22, 1)
                   Else 'Pregunta si está en el Q4
                      penetracion(k) = infproducto(23, 1)

                   End If

                ElseIf k <= (24 + infproducto(7, 1) - mesanual) Then 'Si es la penetración del segundo año

                    If k <= (12 + infproducto(7, 1) - mesanual) + infproducto(26, 1) Then 'mes primer año + plazo del año 2 + 1

                      If k = (12 + infproducto(7, 1) - mesanual) + 1 Then
                         penetracion(k) = infproducto(24, 1)
                      Else
                         penetracion(k) = penetracion(k - 1) + ((infproducto(25, 1) - infproducto(24, 1)) / (infproducto(26, 1) - 1))
                      End If

                    Else 'Después del tiempo de crecimiento

                      penetracion(k) = penetracion(k - 1) 'Seguirá constante de ahí en adelante

                    End If

                Else 'penetración desde el tercer año

                    If k <= (24 + infproducto(7, 1) - mesanual) + infproducto(29, 1) Then 'mes segundo año + plazo del año 3 + 1

                      If k = (24 + infproducto(7, 1) - mesanual) + 1 Then
                         penetracion(k) = infproducto(27, 1)
                      Else
                         penetracion(k) = penetracion(k - 1) + ((infproducto(28, 1) - infproducto(27, 1)) / (infproducto(29, 1) - 1))
                      End If

                    Else
                      penetracion(k) = penetracion(k - 1) 'Seguirá constante de ahí en adelante
                    End If

                End If
         End If
     End If
Next k

'Acá termina generación de la penetración ******************************************************************************************************************************************************

For k = 1 To meses 'Recorrido para los nuevos

      'Calculo de los nuevos clientes
      nuevos(k) = penetracion(k) * infproducto(36, k) 'Porcentaje de participación por el desembolso por el porcentaje de decaimiento


       If infproducto(5, 1) = 1 Then 'Si es prima mensual. Nueva ----------------------------------------------------------------------------------------------


            For t = 1 To k

                If t = k Then 'Consolidación de los nuevos
                   cancel(k, t) = 0
                   vig(k, t) = nuevos(k)
                   vigentes(k) = vigentes(k) + vig(k, t)
                   'Los incentivos se calcularan de otra manera ya que estos no se difieren
                Else

                     'Condición para el cutoff
                     If k >= tcutoff And tcutoff > 0 Then
                        cancel(k, t) = 0
                     Else
                        cancel(k, t) = vig(k - 1, t) * infproducto(8, 1)
                     End If

                     If k < (infproducto(4, 1) + t) Then
                        vig(k, t) = vig(k - 1, t) - cancel(k, t)
                     Else 'Después de cumplida la duración no debería haber mas vigentes de esa cosecha
                       vig(k, t) = 0
                     End If

                     'Condición para el cutoff
                     If k >= tcutoff And tcutoff > 0 Then
                        vigentes(k) = 0
                     Else
                        vigentes(k) = vigentes(k) + vig(k, t)
                     End If

                End If

           cancela(k) = cancela(k) + cancel(k, t)

           Next t

       ElseIf infproducto(5, 1) = 2 Then 'Tipo de prima anual. Nueva --------------------------------------------------------------------------------------------

           For t = 1 To k

                 If t = k Then 'Consolidaación de los nuevos
                    cancel(k, t) = 0
                    vig(k, t) = nuevos(k)
                    vigentes(k) = vigentes(k) + vig(k, t)


                 Else

                    If ((k - t) Mod 12) = 0 Then   'Caida adicional generada por las renovaciones

                      'Condición para el cutoff
                      If k >= tcutoff And tcutoff > 0 Then
                         cancel(k, t) = 0
                      Else
                         cancel(k, t) = vig(k - 1, t) * (infproducto(8, 1) + caidaren) 'Tendrá en cuenta la caida normal del mes, más la caida adicional de las renovaciones
                      End If

                        If k < (infproducto(4, 1) + t) Then 'Si es antes de la duración
                          vig(k, t) = vig(k - 1, t) - cancel(k, t)
                        Else 'Después de cumplida la duración no debería haber mas vigentes de esa cosecha
                          vig(k, t) = 0
                        End If

                      'Condición para el cutoff
                      If k >= tcutoff And tcutoff > 0 Then
                        vigentes(k) = 0

                      Else
                        vigentes(k) = vigentes(k) + vig(k, t)

                      End If

                    Else 'Si no es una renovación

                        'Condición para el cutoff
                        If k >= tcutoff And tcutoff > 0 Then
                           cancel(k, t) = 0
                        Else
                           cancel(k, t) = vig(k - 1, t) * infproducto(8, 1)
                        End If

                      If k < (infproducto(4, 1) + t) Then 'Si es antes de la duración
                        vig(k, t) = vig(k - 1, t) - cancel(k, t)
                      Else 'Después de cumplida la duración no debería haber mas vigentes de esa cosecha
                        vig(k, t) = 0
                      End If


                      'Condición para el cutoff
                      If k >= tcutoff And tcutoff > 0 Then
                        vigentes(k) = 0

                      Else
                        vigentes(k) = vigentes(k) + vig(k, t)


                      End If


                    End If

                 End If

                 'Para que genere el valor de la prima promedio antes y después de los 12 meses
                 yvlrp = (t Mod 12)
                 If k > 12 And t <= k Then

                        If t = 1 Then

                           If infproducto(34, 1) = "Si" Then
                             vlrprimac(k, t) = vlrprimac(k - 12, t) * (1 + ipc)
                             vlrprimad(k, t) = vlrprimad(k - 12, t) * (1 + ipc)
                           Else
                             vlrprimac(k, t) = vlrprimac(k - 12, t)
                             vlrprimad(k, t) = vlrprimad(k - 12, t)

                           End If

                        ElseIf t > 1 And yvlrp = 1 Then
                             vlrprimac(k, t) = vlrprimac(k, t - 12)
                             vlrprimad(k, t) = vlrprimad(k, t - 12)
                        Else

                             vlrprimac(k, t) = vlrprimac(k - 1, t - 1)
                             vlrprimad(k, t) = vlrprimad(k - 1, t - 1)

                        End If

                 Else

                 'De lo contrario toma el valor de la prima que ya generó en el primer recorrido arriba

                 End If

              cancela(k) = cancela(k) + cancel(k, t)

           Next t

       ElseIf infproducto(5, 1) = 3 Then  'Tipo de prima unica. Nueva ---------------------------------------------------------------------------------------------------------------------------

                For t = 1 To k

                 If t = k Then
                  cancel(k, t) = 0
                  vig(k, t) = nuevos(k)
                  vigentes(k) = vigentes(k) + vig(k, t)

                 Else

                  If k < (t + infproducto(4, 1) + Mesgarantia) Then 't más la duración + meses garantìa

                     'Condición para el cutoff
                     If k >= tcutoff And tcutoff > 0 Then
                        cancel(k, t) = 0
                     Else
                        cancel(k, t) = vig(k - 1, t) * infproducto(8, 1)
                     End If

                    vig(k, t) = vig(k - 1, t) - cancel(k, t)

                  Else
                    cancel(k, t) = 0
                    vig(k, t) = 0
                  End If

                      'Condición para el cutoff
                      If k >= tcutoff And tcutoff > 0 Then
                        vigentes(k) = 0

                      Else
                        vigentes(k) = vigentes(k) + vig(k, t)

                      End If


                 End If

           cancela(k) = cancela(k) + cancel(k, t)

           Next t

       ElseIf infproducto(5, 1) = 4 Then  'Tipo de prima amortizada. Nueva ----------------------------------------------------------------

'Escritura de la amortizada ---------------------------------------------------------------------------------------------------------------
       'Si el tipo de amortizaciòn es mensual
         If amortiz(i) = "Natural" Then 'Agarra el error si encuentra un producto mal clasificado:
           MsgBox ("Hay un error clasificando un producto en amortizacion")
           GoTo 10000 'Saltar al final del procedimiento
         Else

           For t = 1 To k

               If t = k Then

                    cancel(k, t) = 0
                    vig(k, t) = nuevos(k)
                    vigentes(k) = vigentes(k) + vig(k, t)

               Else

                  If k < (t + infproducto(4, 1)) Then 't más la duración. No se espera que se vendan con garantia extendida

                     'Condición para el cutoff
                     If k >= tcutoff And tcutoff > 0 Then
                        cancel(k, t) = 0
                     ElseIf ((k - t) Mod amortiz(i)) = 1 And (k - t) > 1 Then
                        cancel(k, t) = vig(k - 1, t) * infproducto(8, 1)

                     Else
                        cancel(k, t) = cancel(k - 1, t) + (vig(k - 1, t) * infproducto(8, 1))
                     End If

                  'calculo de los vigentes:----------------------------------------------------------------------------------
                  vig(k, t) = vig(k - 1, t) - (vig(k - 1, t) * infproducto(8, 1))

                  Else 'Despues de la duracion todo debe ser cero
                    cancel(k, t) = 0
                    vig(k, t) = 0

                  End If

                  'Condición para el cutoff
                  If k >= tcutoff And tcutoff > 0 Then
                    vigentes(k) = 0
                  Else
                    vigentes(k) = vigentes(k) + vig(k, t)
                   End If

               End If


           'Crear el valor de la prima despues de los meses de amortizacion------------------------------------------------------------
           If k > amortiz(i) And t <= k Then

              If t = 1 Then

                       If infproducto(34, 1) = "Si" Then
                          vlrprimac(k, t) = vlrprimac(k - amortiz(i), t) * (1 + ipc)
                          vlrprimad(k, t) = vlrprimad(k - amortiz(i), t) * (1 + ipc)
                        Else
                          vlrprimac(k, t) = vlrprimac(k - amortiz(i), t)
                          vlrprimad(k, t) = vlrprimad(k - amortiz(i), t)

                        End If

                        ElseIf t > 1 And yvlrp = 1 Then
                             vlrprimac(k, t) = vlrprimac(k, t - amortiz(i))
                             vlrprimad(k, t) = vlrprimad(k, t - amortiz(i))
                        Else

                             vlrprimac(k, t) = vlrprimac(k - 1, t - 1)
                             vlrprimad(k, t) = vlrprimad(k - 1, t - 1)

                        End If

                 Else

                 'De lo contrario toma el valor de la prima que ya generó en el primer recorrido arriba

           End If


           'Sumatoria de los cancelados por mes
           cancela(k) = cancela(k) + cancel(k, t)



           Next t
         End If

       Else 'Si el tipo de prima es multiprima --------------------------------------------------------------------------------------------

           'Si el tipo de amortizaciòn es mensual
         If amortiz(i) = "Natural" Then 'Agarra el error si encuentra un producto mal clasificado:
           MsgBox ("Hay un error clasificando un producto en multiprima")
           GoTo 10000 'Saltar al final del procedimiento
         Else

           For t = 1 To k

               If t = k Then
                  cancel(k, t) = 0
                  vig(k, t) = nuevos(k)
                  vigentes(k) = vigentes(k) + vig(k, t)

               Else

                  If k < (t + infproducto(4, 1)) Then 't más la duración. No se espera que se vendan con garantia extendida

                     'Condición para el cutoff
                     If k >= tcutoff And tcutoff > 0 Then
                        cancel(k, t) = 0
                     Else
                        cancel(k, t) = vig(k - 1, t) * infproducto(8, 1)
                     End If

                  'calculo de los vigentes:----------------------------------------------------------------------------------
                  vig(k, t) = vig(k - 1, t) - cancel(k, t)

                  Else 'Despues de la duracion todo debe ser cero
                    cancel(k, t) = 0
                    vig(k, t) = 0

                  End If

                  'Condición para el cutoff
                  If k >= tcutoff And tcutoff > 0 Then
                     vigentes(k) = 0
                  Else
                     vigentes(k) = vigentes(k) + vig(k, t)
                  End If

               End If

               'Consolidacion de los cancelados:
               cancela(k) = cancela(k) + cancel(k, t)

           Next t
         End If

'------------------------------------------------------------------------------------------------------------------------------------------
       End If


'Siniestros-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 sinies(k) = infproducto(9, 1) * vigentes(k)

     'GWP, primas emitidas: calculo por tipo de prima -----------------------------------------------------------------------------------------------------------------------------------------

           If infproducto(5, 1) = 1 Then 'si la prima resulta ser mensual = 1 --------------------------------------------------------------------------------------------------------------

               'Pregunta si le aplica o no el IPC
               If infproducto(34, 1) = "Si" Then

                   y = WorksheetFunction.RoundDown(((k - 1) / 12), 0)
                   'Condición para el cutoff
                   If k = tcutoff And tcutoff > 0 Then
                      gwp(k) = -upr(k - 1)
                      gwpn(k) = 0
                   Else
                     gwp(k) = vigentes(k) * infproducto(6, 1) * ((1 + ipc) ^ y) 'vigentes por el valor de la prima
                     gwpn(k) = 0
                   End If


               Else
                  gwp(k) = vigentes(k) * infproducto(6, 1) 'vigentes por el valor de la prima
                  gwpn(k) = 0
               End If

               'Cálculo de la reserva requerida mensual, UPR_eop
               If infproducto(3, 1) = 3 Then 'Todo lo que sea compulsory no debe reservar, se devenga todo ese mismo mes
                 upr(k) = 0
               Else
                 upr(k) = gwp(k) * 0.5
               End If


               If k = 1 Then
                  earnedP(i, k) = gwp(k) - upr(k)
               Else
                  earnedP(i, k) = gwp(k) - upr(k) + upr(k - 1)

               End If


           ElseIf infproducto(5, 1) = 2 Then 'Si la prima resulta ser anual = 2 ---------------------------------------------------------------------------------------------------------------------------------

                 For t = 1 To k

                    If k > 12 And k > t Then  'para las renovaciones

                      If ((k - t) Mod 12) = 0 And k > infproducto(7, 1) Then

                         'Pregunta si le aplica o no el IPC
                         If infproducto(34, 1) = "Si" Then

                            y = WorksheetFunction.RoundDown(((k - 1) / 12), 0)

                            'Condición para el cutoff
                            If k >= tcutoff And tcutoff > 0 Then
                                gwpst(k, t) = 0
                            Else
                                gwpst(k, t) = vig(k, t) * infproducto(6, 1) * ((1 + ipc) ^ y) 'Considera los clientes renovados
                            End If
                         Else

                            'Condición para el cutoff
                            If k >= tcutoff And tcutoff > 0 Then
                                gwpst(k, t) = 0
                            Else
                                gwpst(k, t) = vig(k, t) * infproducto(6, 1) 'Considera los clientes renovados y los nuevos del mismo mes
                           End If

                         End If

                      Else
                      gwpst(k, t) = 0
                      End If

                    Else

                    gwpst(k, t) = 0 'para antes de los 12 meses que no generan prima.
                    gwps(k) = gwps(k) + gwpst(k, t)

                    End If

                    'para cualquier momento del tiempo
                    gwps(k) = gwps(k) + gwpst(k, t)  'acumula la prima positiva
                    gwpnt(k, t) = cancel(k, t) * vlrprimac(k - 1, t)
                    gwpn(k) = gwpn(k) + gwpnt(k, t)
                    uprt(k, t) = vig(k, t) * vlrprimad(k, t) 'considera los nuevos, porque estos seràn los vigentes del primer mes

                     'Condiciòn del cutoff
                     If k >= tcutoff And tcutoff > 0 Then
                      upr(k) = 0
                     Else
                      upr(k) = upr(k) + uprt(k, t) 'Agrupa toda la reserva de todas las cosechas
                     End If

                  Next t

                       'Obtiene la prima emitida neta
                       y = WorksheetFunction.RoundDown(((k - 1) / 12), 0)

                       If infproducto(34, 1) = "Si" Then
                          x = nuevos(k) * infproducto(6, 1) * ((1 + ipc) ^ y)
                       Else
                          x = nuevos(k) * infproducto(6, 1)
                       End If

                       'Condición para el cutoff
                       If k = tcutoff And tcutoff > 0 Then
                         gwp(k) = -upr(k - 1)
                       Else
                         gwp(k) = gwps(k) + x - gwpn(k)
                       End If

                    If k = 1 Then
                      earnedP(i, k) = gwp(k) - upr(k)
                    Else
                      earnedP(i, k) = gwp(k) - upr(k) + upr(k - 1)
                    End If


          ElseIf infproducto(5, 1) = 3 Then 'Si la prima resulta ser única = 3. Nueva --------------------------------------------------------------------------------------------------------------------------------------------------

                  For t = 1 To k

                    If (k - t) < Mesgarantia Then

                        gwpst(k, t) = 0 'Siempre será cero porque no habrá renovaciones
                        gwps(k) = gwps(k) + gwpst(k, t)
                        gwpnt(k, t) = cancel(k, t) * infproducto(6, 1)
                        gwpn(k) = gwpn(k) + gwpnt(k, t)

                        uprt(k, t) = vig(k, t) * infproducto(6, 1) 'considera los nuevos, porque estos seràn los vigentes del primer mes

                        'Condiciòn del cutoff
                        If k >= tcutoff And tcutoff > 0 Then
                          upr(k) = 0
                        Else
                          upr(k) = upr(k) + uprt(k, t) 'Agrupa toda la reserva de todas las cosechas
                        End If


                    Else
                        gwpst(k, t) = 0 'Siempre será cero porque no habrá renovaciones
                        gwps(k) = gwps(k) + gwpst(k, t)
                        gwpnt(k, t) = cancel(k, t) * vlrprimac(k - Mesgarantia - 1, t)
                        gwpn(k) = gwpn(k) + gwpnt(k, t)

                        uprt(k, t) = vig(k, t) * vlrprimad(k - Mesgarantia, t) 'considera los nuevos, porque estos seràn los vigentes del primer mes

                        'Condiciòn del cutoff
                        If k >= tcutoff And tcutoff > 0 Then
                         upr(k) = 0
                        Else
                         upr(k) = upr(k) + uprt(k, t) 'Agrupa toda la reserva de todas las cosechas
                        End If

                     End If

                  Next t


                       'Obtiene la prima emitida neta
                       y = WorksheetFunction.RoundDown(((k - infproducto(7, 1)) / 12), 0)
                       If infproducto(34, 1) = "Si" Then
                          x = nuevos(k) * infproducto(6, 1) * ((1 + ipc) ^ y)
                       Else
                          x = nuevos(k) * infproducto(6, 1)
                       End If

                       'Condición para el cutoff
                       If k = tcutoff And tcutoff > 0 Then
                        gwp(k) = -upr(k - 1)
                       Else
                         gwp(k) = gwps(k) + x - gwpn(k)
                       End If


                      If k = 1 Then
                        earnedP(i, k) = gwp(k) - upr(k)
                      Else
                        earnedP(i, k) = gwp(k) - upr(k) + upr(k - 1)
                      End If

          ElseIf infproducto(5, 1) = 4 Then 'Si la prima resulta ser amortizada 4. Nueva: ----------------------------------------------------------------------------------------------------------------------------------------


                  For t = 1 To k

                    If k > amortiz(i) And k > t Then  'para las renovaciones

                      If ((k - t) Mod amortiz(i)) = 0 And k > infproducto(7, 1) Then

                         'Pregunta si le aplica o no el IPC
                         If infproducto(34, 1) = "Si" Then

                            y = WorksheetFunction.RoundDown(((k - 1) / 12), 0)

                            'Condición para el cutoff
                            If k >= tcutoff And tcutoff > 0 Then
                                gwpst(k, t) = 0

                            ElseIf ((k - t) Mod amortiz(i)) = 0 Then

                               gwpst(k, t) = vig(k, t) * (infproducto(6, 1)) * amortiz(i) * ((1 + ipc) ^ y) 'Considera los clientes renovados
                            Else
                                gwpst(k, t) = 0 'Entre las renovacione no se recibira nada
                            End If
                         Else

                            'Condición para el cutoff
                            If k >= tcutoff And tcutoff > 0 Then
                                gwpst(k, t) = 0
                            Else
                                gwpst(k, t) = vig(k, t) * (infproducto(6, 1)) * amortiz(i)  'Considera los clientes renovados y los nuevos del mismo mes
                           End If

                         End If

                      Else
                        gwpst(k, t) = 0
                      End If

                    Else

                      gwpst(k, t) = 0 'para antes de los meses de amortizacion
                      gwps(k) = gwps(k) + gwpst(k, t)

                    End If

                    'para cualquier momento del tiempo
                    gwps(k) = gwps(k) + gwpst(k, t)  'acumula la prima positiva

                    If ((k - t) Mod amortiz(i)) = 0 Then

                       If infproducto(34, 1) = "Si" Then 'Pregunta de nuevo si debe ser afectado por el IPC
                          y = WorksheetFunction.RoundDown(((k - 1) / 12), 0)
                          gwpnt(k, t) = cancel(k, t) * (infproducto(6, 1)) * amortiz(i) * ((1 + ipc) ^ y)
                       Else
                          gwpnt(k, t) = cancel(k, t) * (infproducto(6, 1)) * amortiz(i)
                       End If
                    Else
                       gwpnt(k, t) = 0
                    End If

                    gwpn(k) = gwpn(k) + gwpnt(k, t)
                    uprt(k, t) = vig(k, t) * vlrprimad(k, t) 'considera los nuevos, porque estos seràn los vigentes del primer mes

                    'Condiciòn del cutoff
                    If k >= tcutoff And tcutoff > 0 Then
                       upr(k) = 0
                    Else
                      upr(k) = upr(k) + uprt(k, t) 'Agrupa toda la reserva de todas las cosechas
                    End If

                 Next t

                    'Obtiene la prima emitida neta
                    y = WorksheetFunction.RoundDown(((k - 1) / 12), 0)

                    If infproducto(34, 1) = "Si" Then
                       x = nuevos(k) * (infproducto(6, 1)) * amortiz(i) * ((1 + ipc) ^ y)
                    Else
                       x = nuevos(k) * (infproducto(6, 1)) * amortiz(i)
                    End If

                    'Condición para el cutoff
                    If k = tcutoff And tcutoff > 0 Then
                       gwp(k) = -upr(k - 1)
                    Else
                       gwp(k) = gwps(k) + x - gwpn(k)
                    End If

                    If k = 1 Then
                      earnedP(i, k) = gwp(k) - upr(k)
                    Else
                      earnedP(i, k) = gwp(k) - upr(k) + upr(k - 1)
                    End If

          Else  'Si la prima resulta ser multiprima 5.------------------------------------------------------------------------------------------------------------------------


                 For t = 1 To k

                    If (k - t) >= amortiz(i) And k > t Then 'para las renovaciones

                       'Condición para el cutoff
                       If k = tcutoff And tcutoff > 0 Then
                          gwp(k) = -upr(k - 1)
                          upr(k) = 0
                          gwpn(k) = 0
                          Else

                          'Pregunta si le aplica o no el IPC
                          If infproducto(34, 1) = "Si" Then
                             y = WorksheetFunction.RoundDown((((k - 1)) / 12), 0)
                             gwp(k) = vigentes(k) * (infproducto(6, 1)) * ((1 + ipc) ^ y) 'vigentes por el valor de la prima
                             gwpn(k) = 0
                          Else
                             gwp(k) = vigentes(k) * infproducto(6, 1) 'vigentes por el valor de la prima
                             gwpn(k) = 0
                          End If

                          'Cálculo de la reserva requerida mensual, UPR_eop
                          If infproducto(3, 1) = 3 Then 'Todo lo que sea compulsory no debe reservar, se devenga todo ese mismo mes
                             upr(k) = 0
                          Else
                             upr(k) = gwp(k) * 0.5
                          End If

                       End If 'Terminacion de la condicion de tcutoff

                       Exit For 'Salga del for de las cosechas porque ya encontro el gwp de ese mes

                    Else 'Antes del mes del cambio, cuando es unica

                        gwpst(k, t) = 0 'Siempre será cero porque no habrá renovaciones
                        gwps(k) = gwps(k) + gwpst(k, t)
                        gwpnt(k, t) = cancel(k, t) * vlrprimac(k - 1, t)
                        gwpn(k) = gwpn(k) + gwpnt(k, t)

                        uprt(k, t) = vig(k, t) * vlrprimad(k, t) 'considera los nuevos, porque estos seràn los vigentes del primer mes

                        'Condiciòn del cutoff
                        If k >= tcutoff And tcutoff > 0 Then
                          upr(k) = 0
                        Else
                          upr(k) = upr(k) + uprt(k, t) 'Agrupa toda la reserva de todas las cosechas
                        End If



                      'Obtiene la prima emitida neta
                       y = WorksheetFunction.RoundDown(((k - infproducto(4, 1)) / 12), 0)
                       If infproducto(34, 1) = "Si" Then
                          x = nuevos(k) * infproducto(6, 1) * amortiz(i) * ((1 + ipc) ^ y)
                       Else
                          x = nuevos(k) * infproducto(6, 1) * amortiz(i)
                       End If

                       'Condición para el cutoff
                       If k = tcutoff And tcutoff > 0 Then
                        gwp(k) = -upr(k - 1)
                       Else
                         gwp(k) = gwps(k) + x - gwpn(k)
                       End If


                    End If

                 Next t

                 'Calculo de la prima devengada
                 If k = 1 Then
                    earnedP(i, k) = gwp(k) - upr(k)
                 Else
                    earnedP(i, k) = gwp(k) - upr(k) + upr(k - 1)
                 End If


          End If 'Termina el condicional de tipo de prima segunda vez

 '------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
           'Obtiene las comisiones
            'Condición para el cutoff
            If k = tcutoff And tcutoff > 0 Then
              commin(k) = -dac(k - 1)
            Else
              commin(k) = gwp(k) * infproducto(10, 1)
            End If

           'Obtiene las comisiones diferidas
           dac(k) = upr(k) * infproducto(10, 1)

           'Obtiene las comisiones devengadas
           If k = 1 Then
             earnedC(i, k) = commin(k) - dac(k)
           Else
             earnedC(i, k) = commin(k) - dac(k) + dac(k - 1)
           End If

           'Iva no descontable
           vatp(k) = infproducto(14, 1) * infproducto(15, 1) * commin(k) * piva
           vata(k) = infproducto(14, 1) * infproducto(15, 1) * earnedC(i, k) * piva

           'Obtiene las incurred claims
           yclaim = WorksheetFunction.RoundUp(((k - infproducto(7, 1) + 1) / 12), 0) 'indicador del año segùn el # del mes

           Select Case yclaim
           Case 1, 2
                incurC(i, k) = earnedP(i, k) * infproducto(11, 1)
           Case 3, 4
                incurC(i, k) = earnedP(i, k) * infproducto(12, 1)
           Case Else
                incurC(i, k) = earnedP(i, k) * infproducto(13, 1)
           End Select


           'Calculo de los ingresos finacieros: *****************************************************************************************************

           'Ingresos financieros por reservas:
           fincomer(k) = (upr(k) - dac(k)) * (((finanp + 1) ^ (1 / 12)) - 1) 'Ingreso financiero mensual

           'Ingreso financiero por capital:
           'Determinar el acumulado de claims de los ùltimos 36 meses:
           If k <= 36 Then
              suminC = suminC + (incurC(i, k) / 3)
           Else
              suminC = suminC + (incurC(i, k) / 3) - (incurC(i, k - 36) / 3)
           End If

           'Determinar el acumulado de GWP de los ùltiumo 12 meses:
           If k <= 12 Then
              sumGwp = sumGwp + gwp(k)
           Else
              sumGwp = sumGwp + gwp(k) - gwp(k - 12)
           End If

           'Ingresos financieros por capital
           reqcap(k) = WorksheetFunction.Max((sumGwp * 0.16), (suminC * 0.26)) 'Calculo de requerimiento de capital
           fincomec(k) = WorksheetFunction.Max((sumGwp * 0.16), (suminC * 0.26)) * (((finanp + 1) ^ (1 / 12)) - 1)
             If (k Mod 12) = 0 Then
                reqcapy(k) = reqcap(k)
             Else
                reqcapy(k) = reqcapy(k)
             End If



           'Calculo de los incentivos y costos de TMK---------------------------------------------------------------------------------------------------------------------
           If infproducto(3, 1) = 1 Or infproducto(3, 1) = 5 Or infproducto(3, 1) = 6 Or infproducto(3, 1) = 8 Or infproducto(3, 1) = 12 Or infproducto(3, 1) = 13 Then 'Si el tipo de oferta es hall, o Garantìa extendida

               yipc = WorksheetFunction.RoundDown((k - 1) / 12, 0) 'Para determinar cuantos años han transcurrido

               If infproducto(5, 1) = 1 Then 'Pregunta el tipo de prima, si es mensual:

                  If infproducto(34, 1) = "Si" Then 'Afectar el valor de la prima promedio por el IPC
                     incentp(k) = infproducto(16, 1) * (infproducto(6, 1) * ((1 + ipc) ^ yipc)) * nuevos(k) 'Incentivo pagado
                  Else
                     incentp(k) = infproducto(16, 1) * infproducto(6, 1) * nuevos(k)  'Incentivo pagado
                  End If

               ElseIf infproducto(5, 1) = 2 Then 'Si es anual

                  If infproducto(34, 1) = "Si" Then
                     incentp(k) = infproducto(16, 1) * ((infproducto(6, 1) * ((1 + ipc) ^ yipc)) / 12) * nuevos(k)
                  Else
                     incentp(k) = infproducto(16, 1) * ((infproducto(6, 1)) / 12) * nuevos(k)
                  End If

               Else 'Si es ùnica
                  If infproducto(34, 1) = "Si" Then
                     incentp(k) = infproducto(16, 1) * ((infproducto(6, 1) * ((1 + ipc) ^ yipc)) / infproducto(4, 1)) * nuevos(k)
                  Else
                     incentp(k) = infproducto(16, 1) * (infproducto(6, 1) / infproducto(4, 1)) * nuevos(k)
                  End If

               End If


           Else 'Si el tipo de oferta es TMKT u otros

              ipctmk = WorksheetFunction.RoundDown((k + mesanual - 2) / 12, 0)
              tmkCost(k) = (infproducto(17, 1) * ((1 + ipc) ^ ipctmk)) * nuevos(k)

           End If

           'Incentivos amortizados
            If k = 1 Then
               incent(k) = incentp(k) - (((upr(k) + gwpn(k)) / infproducto(4, 1)) * infproducto(16, 1))
            Else
               incent(k) = incentp(k) - (((upr(k) + gwpn(k)) / infproducto(4, 1)) * infproducto(16, 1)) + (((upr(k - 1) + gwpn(k)) / infproducto(4, 1)) * infproducto(16, 1))
            End If

           'VAT de incentivos y de costos de TMKT
           If infproducto(3, 1) = 1 Or infproducto(3, 1) = 5 Or infproducto(3, 1) = 6 Or infproducto(3, 1) = 8 Or infproducto(3, 1) = 12 Or infproducto(3, 1) = 13 Then
             If tipincent = "Pagados" Then
                vatincent(k) = infproducto(14, 1) * infproducto(15, 1) * incentp(k) * piva 'VAT pagado de incentivos
             Else
                vatincent(k) = infproducto(14, 1) * infproducto(15, 1) * incent(k) * piva 'VAT amortizado de incentivos
             End If

           Else
              vatmk(k) = infproducto(14, 1) * infproducto(15, 1) * tmkCost(k) * piva
           End If

           'Calculo de ica y 4x1000
           ica(k) = WorksheetFunction.Max(gwp(k) * pica, 0)
           gmf(k) = WorksheetFunction.Max(gwp(k) * pgmf, 0)

indicador = 1000

GoTo 4000

1000 'Indice para regresar del calculo de las aagrupaciones


Next k

'*********************************************************************************************************************************************************************************************************
ElseIf infproducto(19, 1) = "Stock_RRC" Then 'Si resulta ser un tipo de proyección Stock_RRC
'*********************************************************************************************************************************************************************************************************

'Los meses del stock seràn diferentes a los meses de los demàs tipos

  Sheets("RRC").Activate

       'Recorridos para leer el RRC, DAC y vigentes de Stock_RRC
       For cont = 1 To nstocks
        If infproducto(1, 1) = Cells(cont + 1, 1) Then
           For cont1 = 0 To (meses - mesiniciost)

              If cont1 <= 60 Then
                uprstock(cont1) = Cells(cont + 1, cont1 + 3) 'Corresponde al RRC
                dacstock(cont1) = Cells(cont + 1, cont1 + 67)
                vigentestock(cont1) = Cells(cont + 1, cont1 + 132)
              Else
                uprstock(cont1) = uprstock(cont1 - 1) * 0.9
                dacstock(cont1) = dacstock(cont1 - 1) * 0.9
                vigentestock(cont1) = vigentestock(cont1) * 0.9
              End If

           Next cont1

           Exit For 'salga del recorrido porque ya encontró el producto

        End If

       Next cont

For k = 1 To (meses - mesiniciost) 'Este k es del stock. Eso significa que para la herramienta serà k+mesiniciost


       If infproducto(5, 1) = 1 Then 'Si es prima mensual. RRC ------------------------------------------------------------------------------------------------------------------------------------------------

          If k = 1 Then
             cancela(k + mesiniciost) = 0
             vigentes1(k + mesiniciost) = vigentestock(k)
           Else

             If k <= 5 Then 'Condicional para determinar si se le asigna el vector de comportamiento de la caida o no
                  'Condición para el cutoff
                  If k >= tcutoff And tcutoff > 0 Then 'Esto es nùmero de meses desde que se actualiza el Stock
                     cancela(k + mesiniciost) = 0
                  Else
                     cancela(k + mesiniciost) = vigentes1(k + mesiniciost - 1) * (infproducto(8, 1) * vector(k))
                  End If

             Else
                   'Condición para el cutoff
                   If k >= tcutoff And tcutoff > 0 Then
                      cancela(k + mesiniciost) = 0
                   Else
                      cancela(k + mesiniciost) = vigentes1(k + mesiniciost - 1) * infproducto(8, 1)
                   End If

             End If

                 'Condición para el cutoff
                  If k >= tcutoff And tcutoff > 0 Then
                     vigentes1(k + mesiniciost) = 0
                  Else
                     vigentes1(k + mesiniciost) = WorksheetFunction.Max(vigentestock(k) - cancela(k + mesiniciost), 0)
                  End If
          End If

       ElseIf infproducto(5, 1) = 2 Then 'Tipo de prima anual. RRC -----------------------------------------------------------------------------------------------------------------------

           For t = 1 To k

              If k <= 5 Then 'Condicional par determinar si se le asigna el vector de comportamiento de la caida o no

                 If k = 1 Then
                   cancela(k + mesiniciost) = vigentestock(k - 1) * (infproducto(8, 1) * vector(k))
                   vigentes1(k + mesiniciost) = vigentestock(k)
                 Else

                   'Condición para el cutoff
                   If k >= tcutoff And tcutoff > 0 Then
                      cancela(k + mesiniciost) = 0
                      vigentes1(k + mesiniciost) = 0
                   Else
                      cancela(k + mesiniciost) = vigentes1(k + mesiniciost - 1) * (infproducto(8, 1) * vector(k))
                      vigentes1(k + mesiniciost) = WorksheetFunction.Max(vigentestock(k) - cancela(k + mesiniciost), 0)
                   End If

              End If

              Else

                 If k = 1 Then
                   cancela(k + mesiniciost) = vigentestock(k - 1) * infproducto(8, 1)
                   vigentes1(k + mesiniciost) = vigentestock(k)
                 Else
                   cancela(k + mesiniciost) = vigentes1(k + mesiniciost - 1) * infproducto(8, 1)
                   vigentes1(k + mesiniciost) = WorksheetFunction.Max(vigentestock(k) - cancela(k + mesiniciost), 0)
                 End If

              End If

                 'Else 'Para que genere el valor de la prima antes y después de los 12 meses
                 If k > 12 And t <= k Then

                   If t = 1 Then
                    vlrprimac(k, t) = vlrprimac(k - 12, t)
                    vlrprimad(k, t) = vlrprimad(k - 12, t)
                   Else
                    vlrprimac(k, t) = vlrprimac(k - 1, t - 1)
                    vlrprimad(k, t) = vlrprimad(k - 1, t - 1)
                   End If

                 Else

                 End If

           Next t


       Else 'Tipo de prima unica. RRC --------------------------------------------------------------------------------------------------------------------------------------------------------

       'En Stock RRC no hay concepto de cosechas o campañas, así que se coge todo como si suera una mensual

           'For t = 1 To k
               t = k 'igualdad de indices porque no hay cosechas
                 If k = 1 Then
                   cancela(k + mesiniciost) = vigentestock(k - 1) * infproducto(8, 1)
                   vigentes1(k + mesiniciost) = vigentestock(k)
                 Else

                   If k <= 5 Then 'Condicional par determinar si se le asigna el vector de comportamiento de la caida o no.
                      'Condición para el cutoff
                      If k >= tcutoff And tcutoff > 0 Then
                        cancela(k + mesiniciost) = 0
                      Else
                        cancela(k + mesiniciost) = vigentes1(k + mesiniciost - 1) * (infproducto(8, 1) * vector(k))
                      End If

                   Else

                      'Condición para el cutoff
                      If k >= tcutoff And tcutoff > 0 Then
                         cancela(k + mesiniciost) = 0
                      Else
                         cancela(k + mesiniciost) = vigentes1(k + mesiniciost - 1) * infproducto(8, 1)
                      End If

                   End If
                     'Condición para el cutoff
                     If k >= tcutoff And tcutoff > 0 Then
                       vigentes1(k + mesiniciost) = 0
                     Else
                       vigentes1(k + mesiniciost) = WorksheetFunction.Max(vigentestock(k) - cancela(k + mesiniciost), 0)
                     End If


                 End If


                'Para que genere el valor de la prima antes y despues de los 12 meses
                 If k > infproducto(4, 1) And t <= k Then

                   If t = 1 Then
                    vlrprimac(k, t) = vlrprimac(k - infproducto(4, 1), t)
                    vlrprimad(k, t) = vlrprimad(k - infproducto(4, 1), t)

                   Else
                    vlrprimac(k, t) = vlrprimac(k - 1, t - 1)
                    vlrprimad(k, t) = vlrprimad(k - 1, t - 1)
                   End If

                 Else

                 'De lo contrario toma el valor de la prima que ya generò en el primer recorrido arriba

                 End If



           'Next t


       End If 'finaliza tipo de prima

        'sumariza los vigentes de las nuevas ventas + los vigentes que entran como input
        vigentes(k + mesiniciost) = vigentes1(k + mesiniciost) 'Los vigentes1 serán cero porque no hay nuevos para stock_RRC


'Siniestros:

        sinies(k + mesiniciost) = infproducto(9, 1) * vigentes(k + mesiniciost)

'GWP: primas emitidas: calculo por tipo de prima:

           If infproducto(5, 1) = 1 Then 'si la prima resulta ser mensual = 1 --------------------------------------------------------------------------------------------------------------

               gwp(k + mesiniciost) = vigentes1(k + mesiniciost) * infproducto(6, 1) 'vigentes generados por las renovaciones, por el valor de la prima

               'calculo de la reserva requerida mensual, UPR_eop
               upr1(k + mesiniciost) = gwp(k + mesiniciost) * 0.5

                'Condición para el cutoff
                If k >= tcutoff And tcutoff > 0 Then
                   upr(k + mesiniciost) = 0
                Else
                   upr(k + mesiniciost) = upr1(k + mesiniciost) + uprstock(k + mesiniciost)
                End If


               If k = 1 Then
                  earnedP(i, k + mesiniciost) = gwp(k + mesiniciost) - upr(k + mesiniciost) + uprstock(k + mesiniciost - 1)
               Else
                  earnedP(i, k + mesiniciost) = gwp(k + mesiniciost) - upr(k + mesiniciost) + upr(k + mesiniciost - 1)
               End If


              'Obtiene las comisiones
              commin(k + mesiniciost) = gwp(k + mesiniciost) * infproducto(10, 1)
              'Obtiene las comisiones diferidas
              dac(k + mesiniciost) = upr(k + mesiniciost) * infproducto(10, 1)

              'Obtiene las comisiones devengadas de las renovaciones
              If k = 1 Then
                earnedC(i, k + mesiniciost) = earnedP(i, k + mesiniciost) * infproducto(10, 1)
              Else
                earnedC(i, k + mesiniciost) = commin(k + mesiniciost) - dac(k + mesiniciost) + dac(k + mesiniciost - 1)
              End If



           ElseIf infproducto(5, 1) = 2 Then 'Si la prima resulta ser anual = 2 -----------------------------------------------------------------------------------------------------------

                 For t = 1 To k

                    If k > 12 Then

                        gwpst(k + mesiniciost, t) = 0 'Siempre serà cero pòrque no habrà renovaciones
                        gwps(k + mesiniciost) = 0
                        gwpnt(k + mesiniciost, t) = 0
                        uprt(k + mesiniciost, t) = 0
                        upr(k + mesiniciost) = 0
                        gwpn(k + mesiniciost) = 0

                    Else

                    gwpst(k + mesiniciost, t) = 0 'Siempre serà cero pòrque no habrà renovaciones
                    gwps(k + mesiniciost) = gwps(k + mesiniciost) + gwpst(k + mesiniciost, t)
                    gwpnt(k + mesiniciost, t) = cancel(k + mesiniciost, t) * vlrprimac(k - 1, t)
                    uprt(k + mesiniciost, t) = vig(k + mesiniciost, t) * vlrprimad(k, t)   'considera los nuevos, porque estos seràn los vigentes del primer mes

                    'Condición para determinar si es antes o despu'es del efecto de caida del vector
                     If k <= 5 Then

                        If k = 1 Then
                           gwpn(k + mesiniciost) = uprstock(k - 1) * (infproducto(8, 1) * vector(k))
                        Else
                           gwpn(k + mesiniciost) = upr(k + mesiniciost - 1) * (infproducto(8, 1) * vector(k))
                        End If

                     Else 'Despu'es de 5 meses el vector no tendrá efecto

                        If k = 1 Then
                           gwpn(k + mesiniciost) = uprstock(k - 1) * infproducto(8, 1)
                        Else
                           gwpn(k + mesiniciost) = upr(k + mesiniciost - 1) * infproducto(8, 1)
                        End If

                     End If

                        'Condición para el cutoff
                        If k >= tcutoff And tcutoff > 0 Then
                           upr(k + mesiniciost) = 0
                        Else
                           upr(k + mesiniciost) = uprstock(k) - gwpn(k + mesiniciost) 'La reserva en curso por el porcentaje de caida

                        End If

                    End If

                 Next t


                    'Obtiene la prima emitida neta
                    If k <= 12 Then 'para antes de los 12 meses se deben tener en cuenta los nuevos por aparte
                        x = nuevos(k + mesiniciost) * infproducto(6, 1)
                        'Condición para el cutoff
                        If k = tcutoff And tcutoff > 0 Then
                           gwp(k + mesiniciost) = -upr(k + mesiniciost - 1)
                        Else
                           gwp(k + mesiniciost) = gwps(k + mesiniciost) + x - gwpn(k + mesiniciost)
                        End If


                    Else 'para despu-es de 12 meses los nuevos estan incorporados dentro de las renovaciones
                        'Condición para el cutoff
                        If k = tcutoff And tcutoff > 0 Then
                           gwp(k + mesiniciost) = -upr(k + mesiniciost - 1)
                        Else
                           gwp(k + mesiniciost) = gwps(k + mesiniciost) - gwpn(k + mesiniciost)
                        End If


                    End If

                    If k = 1 Then
                      earnedP(i, k + mesiniciost) = gwp(k + mesiniciost) - upr(k + mesiniciost) + uprstock(k - 1)
                    Else
                      earnedP(i, k + mesiniciost) = gwp(k + mesiniciost) - upr(k + mesiniciost) + upr(k + mesiniciost - 1)
                    End If


                    If k > 12 Then

                        commin(k + mesiniciost) = 0
                        dac1(k + mesiniciost) = 0
                        dac(k + mesiniciost) = 0

                        If k = 1 Then
                          earnedC(i, k + mesiniciost) = 0
                        Else
                          earnedC(i, k + mesiniciost) = 0

                        End If

                    Else

                        'Obtiene las comisiones
                        'Condición para el cutoff
                        If k = tcutoff And tcutoff > 0 Then
                          commin(k + mesiniciost) = -dac(k + mesiniciost - 1)
                        Else
                          commin(k + mesiniciost) = gwp(k + mesiniciost) * infproducto(10, 1)
                        End If

                        'Obtiene las comisiones diferidas
                        dac(k + mesiniciost) = upr(k + mesiniciost) * infproducto(10, 1)

                        'Obtiene las comisiones devengadas de las renovaciones
                        If k = 1 Then
                          earnedC(i, k + mesiniciost) = earnedP(i, k + mesiniciost) * infproducto(10, 1)
                        Else
                          earnedC(i, k + mesiniciost) = commin(k + mesiniciost) - dac(k + mesiniciost) + dac(k + mesiniciost - 1)
                        End If

                    End If



           Else 'Si la prima resulta ser única 3 -----------------------------------------------------------------------------------------------------------------------------------------------------------------


                    'Condición para determinar si es antes o despu'es del efecto de caida del vector
                    If k <= 5 Then

                      If k = 1 Then
                         gwpn(k + mesiniciost) = uprstock(k - 1) * (infproducto(8, 1) * vector(k))
                      Else
                        gwpn(k + mesiniciost) = upr(k + mesiniciost - 1) * (infproducto(8, 1) * vector(k))

                      End If

                    Else

                      If k = 1 Then
                         gwpn(k + mesiniciost) = uprstock(k - 1) * infproducto(8, 1)
                      Else
                        gwpn(k + mesiniciost) = upr(k + mesiniciost - 1) * infproducto(8, 1)
                      End If
                    End If

                     'Condición para el cutoff
                     If k >= tcutoff And tcutoff > 0 Then
                        upr(k + mesiniciost) = 0
                     Else

                       If k - 1 < Mesgarantia Then
                          If k = 1 Then
                             upr(k + mesiniciost) = uprstock(k - 1) - gwpn(k + mesiniciost) 'La reserva en curso por el porcentaje de caida
                          Else
                             upr(k + mesiniciost) = upr(k + mesiniciost - 1) - gwpn(k + mesiniciost) 'La reserva en curso por el porcentaje de caida
                          End If
                       Else 'Si es despues de los meses de garantìa
                          upr(k + mesiniciost) = uprstock(k) - gwpn(k + mesiniciost) 'La reserva en curso por el porcentaje de caida
                       End If


                     End If


                      'Obtiene la prima emitida neta
                      x = nuevos(k + mesiniciost) * infproducto(6, 1)
                      'Condición para el cutoff
                      If k = tcutoff And tcutoff > 0 Then
                         gwp(k + mesiniciost) = -upr(k + mesiniciost - 1)
                      Else
                        gwp(k + mesiniciost) = gwps(k + mesiniciost) + x - gwpn(k + mesiniciost)
                      End If


                    If k = 1 Then
                      earnedP(i, k + mesiniciost) = gwp(k + mesiniciost) - upr(k + mesiniciost) + uprstock(k - 1)
                    Else
                      earnedP(i, k + mesiniciost) = gwp(k + mesiniciost) - upr(k + mesiniciost) + upr(k + mesiniciost - 1)
                    End If

                    'Obtiene las comisiones
                      'Condición para el cutoff
                      If k = tcutoff And tcutoff > 0 Then
                        commin(k + mesiniciost) = -dac(k + mesiniciost - 1)
                      Else
                        commin(k + mesiniciost) = gwp(k + mesiniciost) * infproducto(10, 1)
                      End If

                    'Obtiene las comisiones diferidas
                    dac(k + mesiniciost) = upr(k + mesiniciost) * infproducto(10, 1)

                    'Obtiene las comisiones devengadas de las renovaciones
                    If k = 1 Then
                      earnedC(i, k + mesiniciost) = earnedP(i, k + mesiniciost) * infproducto(10, 1)
                    Else
                      earnedC(i, k + mesiniciost) = commin(k + mesiniciost) - dac(k + mesiniciost) + dac(k + mesiniciost - 1)
                    End If


           End If 'Termina el condicional de tipo de prima segunda vez


           'Iva no descontable
           vatp(k + mesiniciost) = infproducto(14, 1) * infproducto(15, 1) * commin(k + mesiniciost) * piva
           vata(k + mesiniciost) = infproducto(14, 1) * infproducto(15, 1) * earnedC(i, k + mesiniciost) * piva

           'Obtiene las incurred claims
           incurC(i, k + mesiniciost) = earnedP(i, k + mesiniciost) * infproducto(11, 1)


           'Calculo de los ingresos finacieros: *****************************************************************************************************

                'Ingresos financieros por reservas:
                 fincomer(k + mesiniciost) = (upr(k + mesiniciost) - dac(k + mesiniciost)) * (((finanp + 1) ^ (1 / 12)) - 1) 'Ingreso financiero mensual por reservas
                'Determinar el acumulado de claims de los ùltimos 36 meses:
                If k <= 36 Then
                   suminC = suminC + (incurC(i, k + mesiniciost) / 3)
                Else
                   suminC = suminC + (incurC(i, k + mesiniciost) / 3) - (incurC(i, k + mesiniciost - 36) / 3)
                End If

               'Determinar el acumulado de GWP de los ùltiumo 12 meses:

                If k <= 12 Then
                   sumGwp = sumGwp + gwp(k + mesiniciost)
                Else
                   sumGwp = sumGwp + gwp(k + mesiniciost) - gwp(k + mesiniciost - 12)
                End If

           'Ingresos financieros por capital
                reqcap(k + mesiniciost) = WorksheetFunction.Max((sumGwp * 0.16), (suminC * 0.26)) 'Calculo de requerimiento de capital
                fincomec(k + mesiniciost) = WorksheetFunction.Max((sumGwp * 0.16), (suminC * 0.26)) * (((finanp + 1) ^ (1 / 12)) - 1)
                  If (k Mod 12) = 0 Then
                     reqcapy(k + mesiniciost) = reqcap(k + mesiniciost)
                  Else
                     reqcapy(k + mesiniciost) = reqcapy(k + mesiniciost)
                  End If



           'Calculo de ica y 4x1000------------------------------------------------------------------------------------------------
           ica(k + mesiniciost) = WorksheetFunction.Max(gwp(k + mesiniciost) * pica, 0)
           gmf(k + mesiniciost) = WorksheetFunction.Max(gwp(k + mesiniciost) * pgmf, 0)

indicador = 2000

GoTo 4000

2000 'Indice para regresar del calculo de las aagrupaciones


Next k

'*************************************************************************************************************************************************************************************************************************
Else 'Si la prima resulta ser stock normal
'*************************************************************************************************************************************************************************************************************************

'Estos no van a leer nada de la hoja de RRC, todo será manejado por medio de los desembolsos
For k = 1 To (meses - mesiniciost)

         If infproducto(5, 1) = 1 Then 'Si es prima mensual---------------------------------------------------------------------------------------------------------

           'Nuevos: para el tipo stock, hacen referencia a las renovaciones que entran como input a la herramienta. Dependiendo de que si es mensual o anual cambiaría
           nuevos(k + mesiniciost) = 0

           If k = 1 Then

            cancela(k + mesiniciost) = infproducto(36, 0) * infproducto(8, 1) 'Solo funciona para los cancelados mensuales
            vigentes(k + mesiniciost) = infproducto(36, 0) * (1 - infproducto(8, 1))

           Else

                'Condición del tcutoff
                If k >= tcutoff And tcutoff > 0 Then
                    cancela(k + mesiniciost) = 0
                Else
                    cancela(k + mesiniciost) = vigentes(k + mesiniciost - 1) * infproducto(8, 1) 'Solo funciona para los cancelados mensuales
                End If

                If k <= infproducto(4, 1) Then 'Si es antes de la duración
                   vigentes(k + mesiniciost) = vigentes(k + mesiniciost - 1) + nuevos(k + mesiniciost) - cancela(k + mesiniciost)

                Else 'Después de cumplida la duración no debería haber mas vigentes de esa cosecha
                    vigentes(k + mesiniciost) = 0
                End If


           End If


         ElseIf infproducto(5, 1) = 2 Then 'Tipo de prima anual. Stock --------------------------------------------------------------------------------------------

           'Nuevos: para el tipo stock, hacen referencia a las renovaciones que entran como input a la herramienta. Dependiendo de que si es mensual o anual cambiaría
           If k <= infproducto(4, 1) Or (k < tcutoff And tcutoff > 0) Then  'Si es antes de la duración o antes del cutoff
              nuevos(k + mesiniciost) = infproducto(20, 1) * infproducto(36, k) * ((1 - infproducto(8, 1)) ^ k) * (1 - caidaren) 'Porcentaje de participación por el desembolso
           Else
              nuevos(k + mesiniciost) = 0
           End If

           For t = 1 To k

                 If t = k Then
                  cancel(k + mesiniciost, t) = 0
                  vig(k + mesiniciost, t) = nuevos(k + mesiniciost)
                  vigentes(k + mesiniciost) = vigentes(k + mesiniciost) + vig(k + mesiniciost, t)

                 Else

                    If ((k - t) Mod 12) = 0 Then   'Caida adicional generada por las renovaciones

                        'Condición para el cutoff
                        If k >= tcutoff And tcutoff > 0 Then
                           cancel(k + mesiniciost, t) = 0
                        Else
                           cancel(k + mesiniciost, t) = vig(k + mesiniciost - 1, t) * (infproducto(8, 1) + caidaren) 'Tendrá en cuenta la caida normal del mes, más la caida adicional de las renovaciones
                        End If

                        vig(k + mesiniciost, t) = vig(k + mesiniciost - 1, t) - cancel(k + mesiniciost, t)
                        vigentes(k + mesiniciost) = vigentes(k + mesiniciost) + vig(k + mesiniciost, t)

                    Else 'Si no es una renovación

                        If k <= infproducto(4, 1) Then

                           'Condición para el cutoff
                            If k >= tcutoff And tcutoff > 0 Then
                               cancel(k + mesiniciost, t) = 0
                            Else
                               cancel(k + mesiniciost, t) = vig(k + mesiniciost - 1, t) * infproducto(8, 1)
                            End If

                           vig(k + mesiniciost, t) = vig(k + mesiniciost - 1, t) - cancel(k + mesiniciost, t)

                        Else 'Después de cumplida la duración no debería haber mas vigentes de esa cosecha
                          vig(k + mesiniciost, t) = 0
                          cancel(k + mesiniciost, t) = 0

                        End If

                    vigentes(k + mesiniciost) = vigentes(k + mesiniciost) + vig(k + mesiniciost, t)

                    End If
                 End If

                 'Else 'Para que genere el valor de la prima antes y despues de los 12 meses
                 yvlrp = (t Mod 12)
                 If k > 12 And t <= k Then

                        If t = 1 Then

                           If infproducto(34, 1) = "Si" Then
                             vlrprimac(k, t) = vlrprimac(k - 12, t) * (1 + ipc)
                             vlrprimad(k, t) = vlrprimad(k - 12, t) * (1 + ipc)
                           Else
                             vlrprimac(k, t) = vlrprimac(k - 12, t)
                             vlrprimad(k, t) = vlrprimad(k - 12, t)

                           End If

                        ElseIf t > 1 And yvlrp = 1 Then
                             vlrprimac(k, t) = vlrprimac(k, t - 12)
                             vlrprimad(k, t) = vlrprimad(k, t - 12)
                        Else

                             vlrprimac(k, t) = vlrprimac(k - 1, t - 1)
                             vlrprimad(k, t) = vlrprimad(k - 1, t - 1)

                        End If

                 Else

                 'De lo contrario toma el valor de la prima que ya generó en el primer recorrido arriba

                 End If

                 cancela(k + mesiniciost) = cancela(k + mesiniciost) + cancel(k + mesiniciost, t)

           Next t


       Else 'Tipo de prima unica. Stock ---------------------------------------------------------------------------------------------------------------------------

                For t = 1 To k

                 If t = k Then
                  cancel(k, t) = 0
                  vig(k, t) = nuevos(k + mesiniciost)
                  vigentes(k + mesiniciost) = vigentes(k + mesiniciost) + vig(k + mesiniciost, t)

                 Else

                 'No es necesario hacer el ajuste de las cancelaciónes porque no hay prima única cuando es Stock
                   'Condición para el cutoff
                    If k >= tcutoff And tcutoff > 0 Then
                       cancel(k + mesiniciost, t) = 0
                    Else
                       cancel(k + mesiniciost, t) = vig(k + mesiniciost - 1, t) * infproducto(8, 1)
                    End If

                  vig(k + mesiniciost, t) = vig(k + mesiniciost - 1, t) - cancel(k + mesiniciost, t)
                  vigentes(k + mesiniciost) = vigentes(k + mesiniciost) + vig(k + mesiniciost, t)

                 End If

                 cancela(k + mesiniciost) = cancela(k + mesiniciost) + cancel(k + mesiniciost, t)

           Next t


       End If 'finaliza tipo de prima


        'sumariza los vigentes de las nuevas ventas + los vigentes que entran como input
        vigentes(k + mesiniciost) = vigentes(k + mesiniciost) + vigentestock(k) 'Los vigentes stock_RRC para clientes stock será vacio porque no están en la base de la hoja stock

        'Siniestros-----------------------------------------------------------------------------------------------------------------------------------------------------------
        sinies(k + mesiniciost) = infproducto(9, 1) * vigentes(k + mesiniciost)

        'GWP: primas emitidas: calculo por tipo de prima ----------------------------------------------------------------------------------------------------------------------------------------

           If infproducto(5, 1) = 1 Then 'si la prima resulta ser mensual = 1 --------------------------------------------------------------------------------------------------------------

               'Pregunta si le aplica o no el IPC
               If infproducto(34, 1) = "Si" Then

                  'Preguntar si lleva los 6 meses para el primer incremento
                  If k >= (12 - msipc) And k <= (11 + (12 - msipc)) Then
                        'Condición para el cutoff
                        If k = tcutoff And tcutoff > 0 Then
                           gwp(k + mesiniciost) = -upr(k + mesiniciost - 1)
                        Else
                           gwp(k + mesiniciost) = vigentes(k + mesiniciost) * infproducto(6, 1) * (1 + ipc)  'vigentes por el valor de la prima
                        End If

                  Else
                        y = WorksheetFunction.RoundDown(((k + msipc) / 12), 0)
                        'Condición para el cutoff
                        If k = tcutoff And tcutoff > 0 Then
                           gwp(k + mesiniciost) = -upr(k + mesiniciost - 1)
                        Else
                           gwp(k + mesiniciost) = vigentes(k + mesiniciost) * infproducto(6, 1) * ((1 + ipc) ^ y) 'vigentes por el valor de la prima
                        End If
                  End If

               Else
                  'Condición para el cutoff
                  If k = tcutoff And tcutoff > 0 Then
                     gwp(k + mesiniciost) = -upr(k + mesiniciost - 1)
                  Else
                     gwp(k + mesiniciost) = vigentes(k + mesiniciost) * infproducto(6, 1) 'vigentes por el valor de la prima
                  End If


               End If


               'calculo de la reserva requerida mensual, UPR_eop
               If infproducto(3, 1) = 3 Then 'Si es compùlsory se debe devengar todo el mismo mes (supuesto fuerte). Sòlo para mensual.
                 upr1(k + mesiniciost) = 0
               Else
                 upr1(k + mesiniciost) = gwp(k + mesiniciost) * 0.5
               End If

                 upr(k + mesiniciost) = upr1(k + mesiniciost) + uprstock(k + mesiniciost)

               If k = 1 Then
                    earnedP(i, k + mesiniciost) = gwp(k + mesiniciost) - upr(k + mesiniciost) + uprstock(k + mesiniciost - 1)
                    Else
                    earnedP(i, k + mesiniciost) = gwp(k + mesiniciost) - upr(k + mesiniciost) + upr(k + mesiniciost - 1)
               End If

           ElseIf infproducto(5, 1) = 2 Then 'Si la prima resulta ser anual = 2. Stock -----------------------------------------------------------------------------------------------------------

                 For t = 1 To k

                    If k > 12 And k > t Then 'para las renovaciones

                      If ((k - t) Mod 12) = 0 Then

                        'Pregunta si le aplica o no el IPC
                        If infproducto(34, 1) = "Si" Then
                           y = WorksheetFunction.RoundDown(((k - 1) / 12), 0)
                           gwpst(k + mesiniciost, t) = vig(k + mesiniciost, t) * infproducto(6, 1) * ((1 + ipc) ^ y) 'Considera los clientes renovados y los nuevos del mismo mes
                        Else
                           gwpst(k + mesiniciost, t) = vig(k + mesiniciost, t) * infproducto(6, 1) 'Considera los clientes renovados y los nuevos del mismo mes
                        End If

                      Else
                      gwpst(k + mesiniciost, t) = 0
                      End If
                    Else

                    gwpst(k + mesiniciost, t) = 0 'para antes de los 12 meses que no generan prima.
                    gwps(k + mesiniciost) = gwps(k + mesiniciost) + gwpst(k + mesiniciost, t)

                    End If

                    'para cualquier momento del tiempo
                    gwps(k + mesiniciost) = gwps(k + mesiniciost) + gwpst(k + mesiniciost, t) 'acumula la prima positiva
                    gwpnt(k + mesiniciost, t) = cancel(k + mesiniciost, t) * vlrprimac(k - 1, t)
                    gwpn(k + mesiniciost) = gwpn(k + mesiniciost) + gwpnt(k + mesiniciost, t)

                    uprt(k + mesiniciost, t) = vig(k + mesiniciost, t) * vlrprimad(k, t) 'considera los nuevos, porque estos seràn los vigentes del primer mes
                    upr1(k + mesiniciost) = upr1(k + mesiniciost) + uprt(k + mesiniciost, t) 'Agrupa toda la reserva de todas las cosechas

                     'Condición para el cutoff
                      If k >= tcutoff And tcutoff > 0 Then
                         upr(k + mesiniciost) = 0
                      Else
                         upr(k + mesiniciost) = upr1(k + mesiniciost) + uprstock(k + mesiniciost)
                      End If

                    Next t

                        'Obtiene la prima emitida neta
                        x = nuevos(k + mesiniciost) * infproducto(6, 1)
                        'Condición para el cutoff
                        If k = tcutoff And tcutoff > 0 Then
                           gwp(k + mesiniciost) = -upr(k + mesiniciost - 1)
                        Else
                          gwp(k + mesiniciost) = gwps(k + mesiniciost) + x - gwpn(k + mesiniciost)
                        End If

                    If k = 1 Then
                      earnedP(i, k + mesiniciost) = gwp(k + mesiniciost) - upr(k + mesiniciost) + uprstock(k + mesiniciost - 1)
                    Else
                      earnedP(i, k + mesiniciost) = gwp(k + mesiniciost) - upr(k + mesiniciost) + upr(k + mesiniciost - 1)
                    End If


           Else 'Si la prima resulta ser única = 3. Stock  --------------------------------------------------------------------------------------------------------------------------------------------------


                For t = 1 To k

                    gwpst(k + mesiniciost, t) = 0 'Siempre será cero pòrque no habrà renovaciones
                    gwps(k + mesiniciost) = gwps(k + mesiniciost) + gwpst(k, t)

                    If k <= (t + infproducto(4, 1)) Then  't más la duración
                       gwpnt(k, t) = cancel(k + mesiniciost, t) * vlrprimac(k - 1, t)
                       gwpn(k + mesiniciost) = gwpn(k + mesiniciost) + gwpnt(k + mesiniciost, t)
                       uprt(k + mesiniciost, t) = vig(k + mesiniciost, t) * vlrprimad(k, t) 'considera los nuevos, porque estos seràn los vigentes del primer mes
                        'Condición para el cutoff
                        If k >= tcutoff And tcutoff > 0 Then
                           upr(k + mesiniciost) = 0
                        Else
                           upr(k + mesiniciost) = upr(k + mesiniciost) + uprt(k + mesiniciost, t) 'Agrupa toda la reserva de todas las cosechas
                        End If


                    Else

                       gwpnt(k + mesiniciost, t) = 0
                       gwpn(k + mesiniciost) = gwpn(k + mesiniciost) + gwpnt(k + mesiniciost - 1, t)
                       uprt(k + mesiniciost, t) = 0
                        'Condición para el cutoff
                        If k >= tcutoff And tcutoff > 0 Then
                           upr(k + mesiniciost) = 0
                        Else
                           upr(k + mesiniciost) = upr(k + mesiniciost) + uprt(k + mesiniciost, t) 'Agrupa toda la reserva de todas las cosechas
                        End If

                    End If
                  Next t


                  'Obtiene la prima emitida neta
                  x = nuevos(k + mesiniciost) * infproducto(6, 1)

                  'Condición para el cutoff
                  If k = tcutoff And tcutoff > 0 Then
                     gwp(k + mesiniciost) = -upr(k + mesiniciost - 1)
                   Else
                     gwp(k + mesiniciost) = gwps(k + mesiniciost) + x - gwpn(k + mesiniciost)
                  End If


                 If k = 1 Then
                   earnedP(i, k + mesiniciost) = gwp(k + mesiniciost) - upr(k + mesiniciost) + uprstock(k + mesiniciost - 1)
                 Else
                   earnedP(i, k + mesiniciost) = gwp(k + mesiniciost) - upr(k + mesiniciost) + upr(k + mesiniciost - 1)
                 End If


           End If 'Termina el condicional de tipo de prima segunda vez

            'Obtiene las comisiones

            'Condición para el cutoff
            If k = tcutoff And tcutoff > 0 Then
               commin(k + mesiniciost) = -dac(k + mesiniciost - 1)
            Else
               commin(k + mesiniciost) = gwp(k + mesiniciost) * infproducto(10, 1)
            End If

           'Obtiene las comisiones diferidas
           dac1(k + mesiniciost) = upr1(k + mesiniciost) * infproducto(10, 1)


           'Obtiene las comisiones devengadas de las renovaciones
           If k = 1 Then
             earnedC(i, k + mesiniciost) = commin(k + mesiniciost) - dac1(k + mesiniciost)
           Else
             earnedC(i, k + mesiniciost) = commin(k + mesiniciost) - dac1(k + mesiniciost) + dac1(k + mesiniciost - 1)
           End If

           'Iva no descontable
           vatp(k + mesiniciost) = infproducto(14, 1) * infproducto(15, 1) * commin(k + mesiniciost) * piva
           vata(k + mesiniciost) = infproducto(14, 1) * infproducto(15, 1) * earnedC(i, k + mesiniciost) * piva

           'Obtiene las incurred claims
           incurC(i, k + mesiniciost) = earnedP(i, k + mesiniciost) * infproducto(11, 1)


           'Calculo de los ingresos finacieros por los productos RRC: *****************************************************************************************************

           'Ingresos financieros por reservas:
           fincomer(k + mesiniciost) = (upr(k + mesiniciost) - dac(k + mesiniciost)) * (((finanp + 1) ^ (1 / 12)) - 1) 'Ingreso financiero mensual por reservas

           'Determinar el acumulado de claims de los ùltimos 36 meses:
           If k <= 36 Then
              suminC = suminC + (incurC(i, k + mesiniciost) / 3)
           Else
              suminC = suminC + (incurC(i, k + mesiniciost) / 3) - (incurC(i, k + mesiniciost - 36) / 3)
           End If

           'Determinar el acumulado de GWP de los ùltiumo 12 meses:
           If k <= 12 Then
              sumGwp = sumGwp + gwp(k + mesiniciost)
           Else
              sumGwp = sumGwp + gwp(k + mesiniciost) - gwp(k + mesiniciost - 12)
           End If

           'Ingresos financieros por capital
           reqcap(k + mesiniciost) = WorksheetFunction.Max((sumGwp * 0.16), (suminC * 0.26)) 'Calculo de requerimiento de capital
           fincomec(k + mesiniciost) = WorksheetFunction.Max((sumGwp * 0.16), (suminC * 0.26)) * (((finanp + 1) ^ (1 / 12)) - 1)
             If (k Mod 12) = 0 Then
                reqcapy(k + mesiniciost) = reqcap(k + mesiniciost)
             Else
                reqcapy(k + mesiniciost) = reqcapy(k + mesiniciost)
             End If

           'Calculo de ica y 4x1000--------------------------------------------------------------------------------------------
           ica(k + mesiniciost) = WorksheetFunction.Max(gwp(k + mesiniciost) * pica, 0)
           gmf(k + mesiniciost) = WorksheetFunction.Max(gwp(k + mesiniciost) * pgmf, 0)


indicador = 3000

GoTo 4000

3000 'Indice para regresar del calculo de las aagrupaciones

Next k

End If 'Finaliza el condicional de tipo de proyección


GoTo 6000 'Salto para que no entre a sumar de nuevo los grupos de PU
'procedimiento para realizar las acumulaciònes anuales y calcular las variables grupales: *****************************************************************************************************
4000 'ìndice para encontrar el procedimiento de suma de variables


    'Variables para el agrupamiento por PU----------------------------------------------------------------------------------------------------------------------------------------------------------

           'Decidir cual incentivo usar
           If tipincent = "Pagados" Then pagincentivos = incentp(k + mesiniciost) Else pagincentivos = incent(k + mesiniciost)

           nuevosg(k + mesiniciost, pugroup(i)) = nuevosg(k + mesiniciost, pugroup(i)) + nuevos(k + mesiniciost)
           vigenteg(k + mesiniciost, pugroup(i)) = vigenteg(k + mesiniciost, pugroup(i)) + vigentes(k + mesiniciost)
           cancelag(k + mesiniciost, pugroup(i)) = cancelag(k + mesiniciost, pugroup(i)) + cancela(k + mesiniciost)
           siniestrog(k + mesiniciost, pugroup(i)) = siniestrog(k + mesiniciost, pugroup(i)) + sinies(k + mesiniciost)
           GWPg(k + mesiniciost, pugroup(i)) = GWPg(k + mesiniciost, pugroup(i)) + gwp(k + mesiniciost)
           UPRg(k + mesiniciost, pugroup(i)) = UPRg(k + mesiniciost, pugroup(i)) + upr(k + mesiniciost)
           earnedPreg(k + mesiniciost, pugroup(i)) = earnedPreg(k + mesiniciost, pugroup(i)) + earnedP(i, k + mesiniciost)
           coming(k + mesiniciost, pugroup(i)) = coming(k + mesiniciost, pugroup(i)) + commin(k + mesiniciost)
           DACg(k + mesiniciost, pugroup(i)) = DACg(k + mesiniciost, pugroup(i)) + dac(k + mesiniciost)
           earnedCog(k + mesiniciost, pugroup(i)) = earnedCog(k + mesiniciost, pugroup(i)) + earnedC(i, k + mesiniciost)
           incurCg(k + mesiniciost, pugroup(i)) = incurCg(k + mesiniciost, pugroup(i)) + incurC(i, k + mesiniciost)
           'resulTecg(k+ mesiniciost, pugroup(i)) = resulTecg(k+ mesiniciost, pugroup(i)) + ResulTec(k+ mesiniciost)
           VAT_Paidg(k + mesiniciost, pugroup(i)) = VAT_Paidg(k + mesiniciost, pugroup(i)) + vatp(k + mesiniciost)
           VAT_Amortig(k + mesiniciost, pugroup(i)) = VAT_Amortig(k + mesiniciost, pugroup(i)) + vata(k + mesiniciost)
           incentig(k + mesiniciost, pugroup(i)) = incentig(k + mesiniciost, pugroup(i)) + pagincentivos 'Incentivos
           tmktCostg(k + mesiniciost, pugroup(i)) = tmktCostg(k + mesiniciost, pugroup(i)) + tmkCost(k + mesiniciost)
           vatincentg(k + mesiniciost, pugroup(i)) = vatincentg(k + mesiniciost, pugroup(i)) + vatincent(k + mesiniciost) 'VAT de los incentivos
           vatmkg(k + mesiniciost, pugroup(i)) = vatmkg(k + mesiniciost, pugroup(i)) + vatmk(k + mesiniciost)
           overheadg(k + mesiniciost, pugroup(i)) = overheadg(k + mesiniciost, pugroup(i)) + (infproducto(35, 1) * earnedP(i, k + mesiniciost))
           icag(k + mesiniciost, pugroup(i)) = icag(k + mesiniciost, pugroup(i)) + ica(k + mesiniciost)
           gmfg(k + mesiniciost, pugroup(i)) = gmfg(k + mesiniciost, pugroup(i)) + gmf(k + mesiniciost)


If indicador = 1000 Then GoTo 1000
If indicador = 2000 Then GoTo 2000
If indicador = 3000 Then GoTo 3000

6000

'Terminar con el procedimiento ****************************************************************************************************************

'Imprime  la base del OutPut:
Sheets("OutPut").Activate
If ActiveSheet.FilterMode Then ActiveSheet.ShowAllData 'Quitar todos los filtros

'Impresiòn de resultaodos: *************************************************************************************************************************************
For k = 1 To meses

If k > k1 Then 'Sólo empezará a imprimir desde un mes después de la fecha estipulada
   'Determinar si siguen los ingresos financieros o no
        If vigentes(k) <= 0 Then
            fincomer(k) = 0
            reqcap(k) = 0
            fincomec(k) = 0
            reqcapy(k) = 0
        Else
        'No haga nada
        End If

'Se envìan todas las variables necesarias a la funciòn imprimir para que se haga la impresiòn de los resultados
'Sólo serán impresas las variables que no requieren de una acumulación. Las que sí como los impuestos serán enviados a otro procedimiento de impresión.
Call imprimir(ji, k, k1, meses, infproducto(1, 1), infsocio(infproducto(2, 1)), infproducto(18, 1), infoferta(infproducto(3, 1)), inftipoprima(infproducto(5, 1)), infproducto(19, 1), pugroup(i), _
     fechas(k), nuevos(k), vigentes(k), cancela(k), sinies(k), gwp(k), upr(k), earnedP(i, k), commin(k), commin(k) * particomin(1), commin(k) * particomin(2), _
     dac(k), earnedC(i, k), earnedC(i, k) * particomin(1), earnedC(i, k) * particomin(2), incurC(i, k), ResulTec(i, k), vatp(k), vata(k), _
     incent(k), incentp(k), tmkCost(k), ica(k), gmf(k), vatincent(k), vatmk(k), gross2(i, k) + (infproducto(35, 1) * earnedP(i, k)) + ica(k) + gmf(k), infproducto(35, 1) * earnedP(i, k), _
     gross2(i, k), infproducto(33, 1), infproducto(30, 1), infproducto(31, 1), infproducto(32, 1), (k - k1), WorksheetFunction.RoundUp((k / 12), 0), infgrupopu(pugroup(i), 4), _
     gwpn(k), reqcap(k), reqcapy(k), (fincomec(k) + fincomer(k)))
Else
GoTo 8000
End If
8000


'Decidir cual incentivo usar
       If tipincent = "Pagados" Then pagincentivos2 = incentp(k) Else pagincentivos2 = incent(k)

       'GOI sin PU ni ingresos financieros, para precisamente calcular el PU, este despues se agrega:
       gastos(i, k) = (infproducto(35, 1) * earnedP(i, k)) + ica(k) + gmf(k)
       gross1(k) = earnedP(i, k) - earnedC(i, k) - vata(k) - pagincentivos2 - tmkCost(k) - incurC(i, k) - gastos(i, k) - vatincent(k) - vatmk(k)
       capitalcost1(k) = earnedP(i, k) * infgrupopu(pugroup(i), 2) '(EP)*%costo
       pu(k) = (gross1(k) - capitalcost1(k))  'Profit 1
       acumpu(k) = acumpu(k - 1) + pu(k)  'Acum de profit 1
       pu2(k) = acumpu(k) * infgrupopu(pugroup(i), 3)  'Profit 2

       'Utilidad preliminar
       gross2(i, k) = gross1(k) + fincomer(k) + fincomec(k)


'Vaciar las varibales para evitar acumulaciones:-------------------------------------
nuevos(k) = 0
sinies(k) = 0
vigentes(k) = 0
vigentestock(k) = 0

If k = 1 Then
  uprstock(k - 1) = 0
Else
  'No haga nada
End If
uprstock(k) = 0

dacstock(k) = 0
cancela(k) = 0
gwp(k) = 0
gwp(k + mesiniciost) = 0
gwpn(k) = 0
gwps(k) = 0
upr(k) = 0
upr1(k + mesiciost) = 0
dac(k) = 0
incent(k) = 0
incentp(k) = 0
tmkCost(k) = 0
vatincent(k) = 0
vatmk(k) = 0
fincomer(k) = 0
fincomec(k) = 0
suminC = 0
sumGwp = 0
reqcap(k) = 0
'----------------------------------------------------------------------------------------------------------------------------------------------

Next k
ji = ji + 1


Next i 'Continuar con el siguiente producto ***************************************************************************************************


'Calculo de la PU por grupo de PU   -----------------------------------------------------------------------------------------------------------
For i = 1 To ngrupos

   For k = 1 To meses

    goi1(k, i) = earnedPreg(k, i) - earnedCog(k, i) - incurCg(k, i) - VAT_Amortig(k, i) - incentig(k, i) - tmktCostg(k, i) - overheadg(k, i) - icag(k, i) - gmfg(k, i) - vatincentg(k, i) - vatmkg(k, i)
    capitalcost(k, i) = earnedPreg(k, i) * infgrupopu(i, 2) '(EP)*%costo
    profit1g(k, i) = (goi1(k, i) - capitalcost(k, i))

        If k = 1 Then 'Si es el primer mes debe tomar lo ya acumulado que entra como insumo
           acumprofitg(k, i) = profit1g(k, i) + infgrupopu(i, 6)
        Else
           acumprofitg(k, i) = profit1g(k, i) + acumprofitg(k - 1, i)
        End If

    profit2g(k, i) = acumprofitg(k, i) * infgrupopu(i, 3) 'Puede ser negativo tambien 'PU
    purealg(k, i) = profit2g(k, i) - infgrupopu(i, 5) 'Se referirá a la PU_eop que es como la "reserva" ( eop = end of period )
    If k = 1 Then puincurg(k, i) = purealg(k, i) - ((infgrupopu(i, 3) * infgrupopu(i, 6)) - infgrupopu(i, 5)) Else puincurg(k, i) = purealg(k, i) - purealg(k - 1, i)
    acumpurealg(k, i) = infgrupopu(i, 5) 'Sse mantiene constante la PU pagada
    resulTecg(k, i) = earnedPreg(k, i) - earnedCog(k, i) - incurCg(k, i) - puincurg(k, i)
    goi2(k, i) = goi1(k, i) - puincurg(k, i)

Next k
j = j + 1
Next i


'Recorrido para agrupar el resultado tecnico positivo dependiendo de la utilidad de la PU: ----------------------------------------------
For i = 1 To totalproduct
   For k = 1 To meses
     If purealg(k, pugroup(i)) > 0 Then
       ResulTec(i, k) = earnedP(i, k) - earnedC(i, k) - incurC(i, k) 'Resultado tecnico prima
       If ResulTec(i, k) > 0 Then
          ResulTecAcum(k, pugroup(i)) = ResulTecAcum(k, pugroup(i)) + ResulTec(i, k)
       Else
          ResulTecAcum(k, pugroup(i)) = ResulTecAcum(k, pugroup(i))
       End If
     Else
     ResulTecAcum(k, pugroup(i)) = 0
     End If
    Next k
 Next i


'Distribuir la PU para cada uno de los productos que tiene resultado tecnico positivo: ----------------------------------------------------
j = 0
For i = 1 To totalproduct
   For k = 1 To meses

       If purealg(k, pugroup(i)) > 0 Then

            If ResulTec(i, k) > 0 Then
                 pureal(i, k) = (ResulTec(i, k) / ResulTecAcum(k, pugroup(i))) * purealg(k, pugroup(i)) 'Porcentaje de participaciòn*PU_eop del grupo
                 puincur(i, k) = (ResulTec(i, k) / ResulTecAcum(k, pugroup(i))) * puincurg(k, pugroup(i))
            Else
               pureal(i, k) = 0
               puincur(i, k) = 0
            End If
       Else
          pureal(i, k) = 0
          puincur(i, k) = 0

       End If

       ResulTec(i, k) = earnedP(i, k) - earnedC(i, k) - incurC(i, k) - puincur(i, k)

       gross2(i, k) = gross2(i, k) - puincur(i, k)
       gross2m(k) = gross2m(k) + gross2(i, k)

       'Imprimir GOI:
       If k > k1 Then

          Cells((k - k1) + 1 + (meses - k1) * j, 25) = pureal(i, k) 'PU Real
          'Cells((k - k1) + 1 + (meses - k1) * j, 26) = puincur(i, k) 'PU Incurrida
          Cells((k - k1) + 1 + (meses - k1) * j, 26) = ResulTec(i, k) 'RT
          'Cells((k - k1) + 1 + (meses - k1) * j, 37) = gross2(i, k) + gastos(i, k) - Cells((k - k1) + 1 + (meses - k1) * j, 50) 'NBI
          'Cells((k - k1) + 1 + (meses - k1) * j, 39) = gross2(i, k) 'GOI

       Else
       'No haga nada
       End If


       'Antes de calcular los impuestos es necesario hacer la suma del GOI (+) por cada mes de todos los productos, para poder determinar la reparticiòn por socio
       If gross2(i, k) > 0 Then
          Acumgross2(k) = Acumgross2(k) + gross2(i, k)
       Else
          Acumgross2(k) = Acumgross2(k)
       End If

   Next k
j = j + 1
Next i


'Después de las primera impresión sigue la de variables calculadas por acumulados ----------------------------------------------------
j = 0
For i = 1 To totalproduct
   For k = 1 To meses

       Acumtax(0) = 0
       Acumtaxrealm(0) = 0

       'Cálculo de los impuestos -----------------------------------------------------------------------------------------------------
       tax(k) = gross2m(k) * taxr 'Tax nominal
       Acumtax(k) = Acumtax(k - 1) + tax(k)

       'Determinar los impuestos del mes
       If Acumtax(k) > 0 And Acumtax(k - 1) > 0 Then
          taxrealm(k) = WorksheetFunction.Max(Acumtax(k) - Acumtaxrealm(k - 1), 0)
       Else
          taxrealm(k) = WorksheetFunction.Max(Acumtax(k), 0)
       End If

       Acumtaxrealm(k) = Acumtaxrealm(k - 1) + taxrealm(k)

       'Distribuir los impuestos por socio
       If gross2(i, k) > 0 Then
          taxreal(i, k) = taxrealm(k) * (gross2(i, k) / Acumgross2(k))
       Else
          taxreal(i, k) = 0
       End If


      'Imprimir el impuesto
      If k > k1 Then

      'Cells((k - k1) + 1 + (meses - k1) * j, 40) = taxreal(i, k) 'taxes

      Else
      'No haga nada
      End If
  Next k
j = j + 1

Next i


'Copiar la información de base real y colocarla en el output si se elige dicha opción
If Sheets("Consola").Cells(13, 3) = "No" Then GoTo 5000

Call pegarreal

5000 'Salto del pegado de los resultados reales

Application.ScreenUpdating = True

tfinal = DateTime.Now
ttotal = tfinal - tinicio

Sheets("Consola").Select
Cells(41, 6) = ttotal

MsgBox ("Presupuesto Generado")

10000 'Salto generado por error en amortizacion

End Sub

Sub pegarreal()

'numero de registros en el Output
nfilas = Sheets("OutPut").Range("A1").End(xlDown).Row

'numero de registros en "Base Real"
Sheets("BaseReal").Activate
If ActiveSheet.FilterMode Then ActiveSheet.ShowAllData 'Quitar todos los filtros

nfilas1 = Sheets("BaseReal").Range("C1").End(xlDown).Row - 1

'Copia la formula de actualización de ID
Range("A2").Select
ActiveCell.FormulaR1C1 = "=+MAX(OutPut!C) + 1"
'Formula para siguientes Id's
Range("A3").Select
ActiveCell.FormulaR1C1 = "=+IF(RC[2]=R[-1]C[2],R[-1]C,R[-1]C+1)"
Range("A3").Select
Selection.Copy
Range(Cells(4, 1), Cells(nfilas1 + 1, 1)).Select
ActiveSheet.Paste
Range(Cells(2, 1), Cells(nfilas1 + 1, 1)).Select
Selection.Copy
Selection.PasteSpecial Paste:=xlPasteValues, Operation:=xlNone, SkipBlanks _
        :=False, Transpose:=False

'copiar toda la información
Range(Cells(2, 1), Cells(nfilas1 + 1, 49)).Select
Selection.Copy

'Pasar la información a la pagina de output
Sheets("OutPut").Activate
Cells(nfilas + 1, 1).Select
Selection.PasteSpecial Paste:=xlPasteValues, Operation:=xlNone, SkipBlanks _
        :=False, Transpose:=False

End Sub

Sub imprimir(j, k, k1, meses, id, socio, cod, oferta, tprima, tproyec, grupo, fecha, nuevo, vig, cancel, sinis, gwp, upr, ep, comin, comins, cominb, dac, ec, ecs, ecb, ic, _
    rt, vatp, vata, incent, incentp, tmk, ica, gmf, vati, vatmk, gros2, over, goi, ln, cj, capa, nombre, mp, ap, ngrupo, gwpn, reqc, reqca, fincon)

       Cells((k - k1) + 1 + (meses - k1) * j, 1) = id 'Id_Producto
       Cells((k - k1) + 1 + (meses - k1) * j, 2) = socio 'Nombre del socio llamado por el Id_socio
       Cells((k - k1) + 1 + (meses - k1) * j, 3) = cod 'Cod_Producto
       Cells((k - k1) + 1 + (meses - k1) * j, 4) = oferta 'Id_T.Ofertas
       Cells((k - k1) + 1 + (meses - k1) * j, 5) = tprima 'Id_T.Prima
       Cells((k - k1) + 1 + (meses - k1) * j, 6) = tproyec 'Tipo_Proyección
       Cells((k - k1) + 1 + (meses - k1) * j, 7) = grupo 'Id_Grupo
       Cells((k - k1) + 1 + (meses - k1) * j, 8) = fecha 'Fecha
       Cells((k - k1) + 1 + (meses - k1) * j, 9) = nuevo 'Nuevos
       Cells((k - k1) + 1 + (meses - k1) * j, 10) = vig 'Vigentes
       Cells((k - k1) + 1 + (meses - k1) * j, 11) = cancel 'Cancelados
       Cells((k - k1) + 1 + (meses - k1) * j, 12) = sinis 'Siniestros
       Cells((k - k1) + 1 + (meses - k1) * j, 13) = gwp 'GWP: Primas emitidas
       Cells((k - k1) + 1 + (meses - k1) * j, 14) = gwpn 'Valor de las cancelaciones
       Cells((k - k1) + 1 + (meses - k1) * j, 15) = upr 'UPR_eop
       Cells((k - k1) + 1 + (meses - k1) * j, 16) = ep 'Earned Premium
       Cells((k - k1) + 1 + (meses - k1) * j, 17) = comin 'Comisiones
       Cells((k - k1) + 1 + (meses - k1) * j, 18) = comins 'Comisiones de socio
       Cells((k - k1) + 1 + (meses - k1) * j, 19) = cominb 'Comisiones de broker
       Cells((k - k1) + 1 + (meses - k1) * j, 20) = dac 'Comisiones diferidas
       Cells((k - k1) + 1 + (meses - k1) * j, 21) = ec 'Comisiones devengadas
       Cells((k - k1) + 1 + (meses - k1) * j, 22) = ecs 'Comisiones devengadas de socio
       Cells((k - k1) + 1 + (meses - k1) * j, 23) = ecb 'Comisiones devengadas de broker
       Cells((k - k1) + 1 + (meses - k1) * j, 24) = ic 'Incurred Claims
       'Cells((k - k1) + 1 + (meses - k1) * j, 25) = pu 'PU_eop
       'Cells((k - k1) + 1 + (meses - k1) * j, 26) = pui 'PU incurrida del mes
       Cells((k - k1) + 1 + (meses - k1) * j, 26) = rt 'Resultado Tecnico
       Cells((k - k1) + 1 + (meses - k1) * j, 33) = vatp 'IVA no descontable pagado
       Cells((k - k1) + 1 + (meses - k1) * j, 34) = vata 'IVA no descontable amortizado
       'Cells((k - k1) + 1 + (meses - k1) * j, 30) = incent 'Incentivos amortizado
       'Cells((k - k1) + 1 + (meses - k1) * j, 31) = incentp 'Incentivo pagado
       'Cells((k - k1) + 1 + (meses - k1) * j, 32) = tmk 'Costo de TMKT
       'Cells((k - k1) + 1 + (meses - k1) * j, 33) = ica 'Impuesto del ICA
       'Cells((k - k1) + 1 + (meses - k1) * j, 34) = gmf 'el 4x1000
       'Cells((k - k1) + 1 + (meses - k1) * j, 35) = vati 'vat de incentivos
       'Cells((k - k1) + 1 + (meses - k1) * j, 36) = vatmk 'Vat de tmk
       'Cells((k - k1) + 1 + (meses - k1) * j, 37) = gros2 'NBI
       'Cells((k - k1) + 1 + (meses - k1) * j, 38) = over '% overheads*EP
       'Cells((k - k1) + 1 + (meses - k1) * j, 39) = goi 'GOI de cada producto
       'Cells((k - k1) + 1 + (meses - k1) * j, 40) = tx 'taxes
       'Cells((k - k1) + 1 + (meses - k1) * j, 27) = WorksheetFunction.Max(goi - tx, 0) 'NOI
       Cells((k - k1) + 1 + (meses - k1) * j, 27) = ln 'Linea negocio socio
       Cells((k - k1) + 1 + (meses - k1) * j, 28) = cj 'Oferta CJ
       Cells((k - k1) + 1 + (meses - k1) * j, 29) = capa 'Capa
       Cells((k - k1) + 1 + (meses - k1) * j, 30) = nombre 'Nombre del producto
       Cells((k - k1) + 1 + (meses - k1) * j, 31) = mp 'Mes de proyeccìon
       Cells((k - k1) + 1 + (meses - k1) * j, 32) = ap 'Año de proyección
       'Cells((k - k1) + 1 + (meses - k1) * j, 47) = ngrupo 'Nombre del grupo
       'Cells((k - k1) + 1 + (meses - k1) * j, 48) = reqc 'Requerimiento de capital
       'Cells((k - k1) + 1 + (meses - k1) * j, 49) = reqca 'Requerimiento de capital anual
       'Cells((k - k1) + 1 + (meses - k1) * j, 50) = fincon 'Ingreso financiero

End Sub


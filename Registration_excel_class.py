class Registration :
    
    def Register(self,returns,CPPI_values, floor_values,Capital_reinjection,reference_cap,safe_asset_rate,days,DD,Omega_r,Sharp_ratio,Sortino_ratio,information_ratio,M2_Ratio,PSR,CGR,STD,Cst_VaR,Actualized_Expected_Shortfall,Actualized_Var,Beta,jensen_alpha,Max_drawdown,cum_returns):       
        
        exportList=pd.DataFrame({'Benchmark':CPPI_values.iloc[0,0]*(1+returns).cumprod().iloc[:,0],'TPPI':CPPI_values.iloc[:,0], "Floor":floor_values.iloc[:,0],"Reference Capital":reference_cap.iloc[:,0],"Capital reinjection":Capital_reinjection.iloc[:,0]
                                 ,"Drawdowns":DD.iloc[:,0]}
                                ,index = reference_cap.index).fillna(0)

        
        exportList2 = pd.DataFrame({"Actualized VaR 5%":Actualized_Var.iloc[:,0],"Actualized Expected Shortfall 5%":Actualized_Expected_Shortfall.iloc[:,0],"Constant VaR 5%":Cst_VaR.iloc[:,0]},index = Actualized_Var.index)
        
        exportList3 = pd.DataFrame({"Sharpe Ratio":Sharp_ratio,"Omega Ratio":Omega_r,"Sortino_ratio":Sortino_ratio,"Information Ratio":information_ratio,"Modigliani Ratio":M2_Ratio,"Probabilistic Sharpe Ratio":PSR,"CAGR":CGR,"Standard deviation":STD,"Beta":Beta,"Jensen alpha":jensen_alpha,"Maximum Drawdown(in %)":Max_drawdown,"Cumulative Returns(in %)":cum_returns},index = ["Ratios"])
        #---------------------------------------------------------------------------------------------------------------------------------------------------
        
        writer = ExcelWriter("ScreenOutput.xlsx")
        exportList.to_excel(writer, "Strategy") #Sheet1
        workbook = writer.book
        worksheet = writer.sheets['Strategy']
        chart = workbook.add_chart({'type': 'line'})
        max_row = len(exportList) + 1
        for i in range(len(exportList.columns[:-1])):
            col = i + 1
            chart.add_series({
                'name':       ['Strategy', 0, col],
                'categories': ['Strategy', 1, 0, max_row, 0],
                'values':     ['Strategy', 1, col, max_row, col],
                'line':       {'width': 1.00},
            })
        # Configure the chart axes.
        chart.set_x_axis({'name': 'Date', 'date_axis': True})
        chart.set_y_axis({'name': 'Amount (in M$)', 'major_gridlines': {'visible': False}})
            
        # Position the legend at the top of the chart.
        chart.set_legend({'position': 'top'})
            
        # Insert the chart into the worksheet.
        worksheet.insert_chart('J2', chart)
        
        chart2 = workbook.add_chart({'type': 'line'})
        max_row = len(exportList) + 1
        for i in range(len(['reinjection'])):
            col = i + 5
            chart2.add_series({
                'name':       ['Strategy', 0, col],
                'categories': ['Strategy', 1, 0, max_row, 0],
                'values':     ['Strategy', 1, col, max_row, col],
                'line':       {'width': 1.00},
            })
        # Configure the chart axes.
        chart2.set_x_axis({'name': 'Date', 'date_axis': True})
        chart2.set_y_axis({'name': 'Amount (in M$)', 'major_gridlines': {'visible': False}})
            
        # Position the legend at the top of the chart.
        chart2.set_legend({'position': 'top'})
            
        # Insert the chart into the worksheet.
        worksheet.insert_chart('X2', chart2)
                
        chart3 = workbook.add_chart({'type': 'line'})
        max_row = len(exportList) + 1
        for i in range(len(['DD'])):
            col = i + 6
            chart3.add_series({
                'name':       ['Strategy', 0, col],
                'categories': ['Strategy', 1, 0, max_row, 0],
                'values':     ['Strategy', 1, col, max_row, col],
                'line':       {'width': 1.00},
            })
            
        # Configure the chart axes.
        chart3.set_x_axis({'name': 'Date', 'date_axis': True})
        chart3.set_y_axis({'name': 'In %', 'major_gridlines': {'visible': False}})
            
        # Position the legend at the top of the chart.
        chart3.set_legend({'position': 'top'})
            
        # Insert the chart into the worksheet.
        worksheet.insert_chart('J25', chart3)
        #---------------------------------------------------------------------------------------------------------------------------------------------------
        
        exportList2.to_excel(writer, "Risk Management")
        workbook = writer.book
        worksheet = writer.sheets['Risk Management']
        chart_var = workbook.add_chart({'type': 'line'})
        max_row = len(exportList2) + 1
        for i in range(len(exportList2.columns)):
            col = i + 1
            chart_var.add_series({
                'name':       ['Risk Management', 0, col],
                'categories': ['Risk Management', 1, 0, max_row, 0],
                'values':     ['Risk Management', 1, col, max_row, col],
                'line':       {'width': 1.00},
            })
        # Configure the chart axes.
        chart_var.set_x_axis({'name': 'Date', 'date_axis': True})
        chart_var.set_y_axis({'name': 'in %', 'major_gridlines': {'visible': False}})
            
        # Position the legend at the top of the chart.
        chart_var.set_legend({'position': 'top'})
            
        # Insert the chart into the worksheet.
        worksheet.insert_chart('G2', chart_var)
        #---------------------------------------------------------------------------------------------------------------------------------------------------
        
        exportList3.to_excel(writer, "Ratios")
        workbook = writer.book
        worksheet = writer.sheets['Ratios']
        chart_ratios = workbook.add_chart({'type': 'line'})
        max_row = len(exportList3) + 1
        for i in range(len(exportList3.columns[:-1])):
            col = i + 1
            chart_ratios.add_series({
                'name':       ['Ratios', 0, col],
                'categories': ['Ratios', 1, 0, max_row, 0],
                'values':     ['Ratios', 1, col, max_row, col],
                'line':       {'width': 1.00},
            })
        
        writer.save()
        
        print("Your document is registred under the name:'ScreenOutput.xlsx'")
        
        return 
    
    def __init__(self,returns,CPPI_values,floor_values,Capital_reinjection,reference_cap,safe_asset_rate,days,DD,Omega_r,Sharp_ratio,Sortino_ratio,information_ratio,M2_Ratio,PSR,CGR,STD,Cst_VaR,Actualized_Expected_Shortfall,Actualized_Var,Beta,jensen_alpha,Max_drawdown,cum_returns):
        self.returns = returns
        self.CPPI_values = CPPI_values
        self.floor_values =floor_values
        self.reference_cap = reference_cap
        self.Capital_reinjection = Capital_reinjection
        self.DD = DD
        self.Omega_r = Omega_r
        self.Sharp_ratio = Sharp_ratio
        self.Sortino_ratio = Sortino_ratio
        self.information_ratio = information_ratio
        self.M2_Ratio = M2_Ratio
        self.PSR = PSR
        self.days = days
        self.Cst_VaR = Cst_VaR
        self.CGR = CGR
        self.STD = STD
        self.Actualized_Expected_Shortfall = Actualized_Expected_Shortfall
        self.Actualized_Var = Actualized_Var
        self.Beta = Beta
        self.jensen_alpha = jensen_alpha
        self.Max_drawdown = Max_drawdown
        self.cum_returns = cum_returns
        self.Registering = self.Register(returns,CPPI_values, floor_values,Capital_reinjection,reference_cap,safe_asset_rate,days,DD,Omega_r,Sharp_ratio,Sortino_ratio,information_ratio,M2_Ratio,PSR,CGR,STD,Cst_VaR,Actualized_Expected_Shortfall,Actualized_Var,Beta,jensen_alpha,Max_drawdown,cum_returns)     

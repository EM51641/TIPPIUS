class Chart:
    
    def Chart(self,returns,tipp,floor_values,ref_cap,reinjection_cap,DD,Actualized_Var,Actualized_Expected_Shortfall,Cst_VaR): 
        fig,axe=plt.subplots()
        chart = tipp.plot(ax=axe,figsize=(12,6), color="blue", legend=True)
        normal =  tipp.iloc[0,0]*(1+returns).cumprod()
        normal.columns = ['Benchmark']
        normal.plot(ax=axe, style='g--', legend=True)
        floor_values.plot(ax=axe, style='red', legend=True)
        ref_cap.plot(ax=axe, style='black', legend=True)
        #reinjection_cap.plot(ax=axe, style='b--', legend=True)
        ax2=axe.twinx()
        reinjection_cap.plot(ax=ax2, style='b--', legend=True)
        # make a plot with different y-axis using second axis object
        #ax2.plot(reinjection_cap,color="red",marker="o")
        ax2.set_ylabel(" Capital Reinjection amount ",color="Black",fontsize=14)
        axe.set_ylabel(" Cumulative Amount ",color="Black",fontsize=14)
        axe.legend(['With TIPP','Without TIPP','Floor','Reference Capital'])
        ax2.legend(['Capital Reinjection'])
        plt.show()
        fig,axe2=plt.subplots()
        B_Drawdown = (normal.div(normal.cummax())-1)*100
        B_Drawdown.columns = ['Benchmark Drawdown in (%)']
        DD.plot(ax=axe2,figsize=(12,6), legend=True)
        B_Drawdown.plot(ax=axe2,figsize=(12,6), legend=True)
        plt.show()
        fig3,axe3=plt.subplots()
        Actualized_Var.plot(ax=axe3,style='g--',figsize=(12,6),legend = True)
        Actualized_Expected_Shortfall.plot(ax=axe3,style='red',legend = True)
        Cst_VaR.plot(ax=axe3,style='black',legend = True)
        plt.show()
        
    def __init__(self,returns,tipp,floor_values,ref_cap,reinjection_cap,DD,Actualized_Var,Actualized_Expected_Shortfall,Cst_VaR):
        self.returns = returns
        self.tipp = tipp
        self.floor_values =floor_values
        self.ref_cap = ref_cap
        self.reinjection_cap = reinjection_cap
        self.Actualized_Var = Actualized_Var
        self.Actualized_Expected_Shortfall = Actualized_Expected_Shortfall
        self.Cst_VaR = Cst_VaR
        self.Charting = self.Chart(returns,tipp,floor_values,ref_cap,reinjection_cap,DD,Actualized_Var,Actualized_Expected_Shortfall,Cst_VaR)

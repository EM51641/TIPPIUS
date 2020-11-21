class Initializing_values:
    
    def __init__(self):
        pass
            
    def Charted(self,breturns, A, B,C,D,VaR_C,CvaR_D,VaR_unc):
        E = self.DD(A.pct_change())
        Chart(breturns,A,B,D,C,E,VaR_C,CvaR_D,VaR_unc).Charting
        
    def Values(self,breturns,safe_asset_rate,Lock_in,Min_risk_part,Capital_reinjection_rate,cppi,floor_percent,m):
        A, B,C,D = TIPP(breturns,safe_asset_rate,Lock_in,Min_risk_part,Capital_reinjection_rate,cppi,floor_percent,m).tppi
        return A,B,C,D
    
    def Rgstr(self,breturns,CPPI_values, floor_values,Capital_reinjection,reference_cap,safe_asset_rate,days,theta,sampled_garch_number_needed):
        
        returns = CPPI_values.pct_change()
        cum_returns = self.Cumulative_r(returns)*100
        E = self.DD(returns)
        Omega_r = self.Omega_ratio(returns)
        Sharp_ratio = self.Sharp_rt(returns,safe_asset_rate,days)
        Sortino_ratio = self.Sortino_rt(returns,safe_asset_rate,days)
        information_ratio = self.information_ratio(returns,breturns,days)
        M2_Ratio = self.modigliani_ratio(returns,breturns,safe_asset_rate,days)
        PSR = self.probabilistic_sharpe_ratio(returns,breturns,safe_asset_rate,days)
        CGR = self.CAGR(returns)
        STD = self.STD(returns,days)
        Actualized_Var,Actualized_Expected_Shortfall,Cst_VaR = self.VaR_Studen_Distribution(returns,theta,sampled_garch_number_needed)
        Beta,jensen_alpha= Initializing_values().jensen_alpha_beta(returns ,Risk_ass,days=52)
        Max_drawdown = E.min()[0]
        Registration(breturns,CPPI_values, floor_values,Capital_reinjection,reference_cap,safe_asset_rate,days,E,Omega_r,Sharp_ratio,Sortino_ratio,information_ratio,M2_Ratio,PSR,CGR,STD,Cst_VaR,Actualized_Expected_Shortfall,Actualized_Var,Beta,jensen_alpha,Max_drawdown,cum_returns).Registering
        return 
    
    def Sharp_rt(self,returns,safe_asset_rate,days):
        Excess_returns = ((returns- safe_asset_rate.values/days).mean()*days)
        strat_std = returns.std()*np.sqrt(days)
        Sharpe_ratio = (Excess_returns/strat_std)[0]
        return Sharpe_ratio
                          
    def Sortino_rt(self,returns,safe_asset_rate,days):
        Sortino_std = returns.mask(returns>=0).std()*np.sqrt(days)
        Excess_returns = ((returns- safe_asset_rate.values/days).mean()*days)
        Sortino_ratio = (Excess_returns/Sortino_std)[0]
        return Sortino_ratio
                          
                          
    def information_ratio(self,returns, breturns, days):
        return_difference = returns - breturns.values
        volatility = return_difference.std() * np.sqrt(days)
        information_ratio = ((return_difference.mean()*days) / volatility)[0]
        return information_ratio
    
    def modigliani_ratio(self,returns, breturns, safe_asset_rate, days):
        #volatility = returns.std() * np.sqrt(days)
        sharpe_ratio = self.Sharp_rt(returns,safe_asset_rate,days)#(returns.mean() - rf) / volatility
        benchmark_volatility = breturns.std() * np.sqrt(days)
        m2_ratio = ((sharpe_ratio * benchmark_volatility)[0] + safe_asset_rate.iloc[-1])[0]
        return m2_ratio
    
    def estimated_sharpe_ratio_stdev(self,returns,safe_asset_rate,days):
        sharpe_ratio = self.Sharp_rt(returns,safe_asset_rate,days)
        n = len(returns)
        skew = pd.Series(scipy_stats.skew(returns), index=returns.columns)
        kurtosis = pd.Series(scipy_stats.kurtosis(returns, fisher=False), index=returns.columns)
        sr_std = np.sqrt((1 + (0.5 * sharpe_ratio ** 2) - (skew * sharpe_ratio) + (((kurtosis - 3) / 4) * sharpe_ratio ** 2)) / (n - 1))
        return sr_std
    
    def probabilistic_sharpe_ratio(self,returns, breturns,safe_asset_rate,days):
        returns = returns.fillna(0)
        sr_std = self.estimated_sharpe_ratio_stdev(returns,safe_asset_rate,days)
        sharpe_ratio = self.Sharp_rt(returns,safe_asset_rate,days)
        sharpe_ratio_benchmark = self.Sharp_rt(breturns,safe_asset_rate,days)
        psr = scipy_stats.norm.cdf((sharpe_ratio - sharpe_ratio_benchmark) / sr_std)[0]
        return psr
    
    def Omega_ratio(self,returns):
        ecdf = ECDF(np.array(returns.dropna().T)[0])
        Omega_ratio = (1-ecdf(0))/ecdf(0)
        return Omega_ratio
    
    def STD(self,returns,days):
        stdev = returns.std()[0] * np.sqrt(days)
        return stdev
    
    def CAGR(self,returns):
        Ending_value = ((1+returns).cumprod()-1)
        Beginning_value = 1
        n = len(returns.resample('1Y').last().index)
        CGR = (Ending_value.iloc[-1,0]/Beginning_value)**(1/n) - 1
        return CGR
    def Cumulative_r(self,returns):
        cum_r = ((1 + returns).dropna().cumprod()-1).iloc[-1,0]
        return cum_r
        
    
    def VaR_Studen_Distribution(self,returns,theta,sampled_garch_number_needed): #500 datas needed 
        f=sampled_garch_number_needed
        l=0
        Constant_VaR=[]
        Q_ratio=[]
        Constant_ES=[]
        Var_MTRX=[]
        ES_MRTX=[]
        
        J=returns.sort_values('Date')
        for g in range(int(round(len(returns.dropna().iloc[f:])/2,0))):
            am = arch_model(returns.dropna().iloc[l:f]*100,vol='Garch', p=1, o=1, q=1,rescale=False,mean='AR', lags=1,dist='StudentsT')
            res = am.fit(update_freq=1,disp='off')
            forecasts = res.forecast(start=returns.index[0], horizon=1)
            z=((returns.iloc[:,0]-forecasts.mean.dropna().iloc[:,0])/(res.conditional_volatility)).dropna()
            z_uploaded=z.iloc[:f].sort_values()*(-1)
            params=t.fit(z_uploaded.dropna())
            df=params[0]
            q_99_t=np.sqrt((df-2)/df)*t.ppf(1-theta,df)
            Var=-((forecasts.mean.dropna().iloc[-1,0])+np.sqrt((forecasts.variance.dropna().iloc[-1,0]))*q_99_t)
            ES=-((((t.pdf(t.ppf(1-theta,df),df))/(theta))*((df+t.ppf(1-theta,df)**2)/(df-1)))*np.sqrt((forecasts.variance.dropna().iloc[-1,0]))-forecasts.mean.dropna().iloc[-1,0])
            l = l + 2
            f = f + 2
            Q_ratio.append(Var/ES)
            Constant_VaR.append(-q_99_t)
            Var_MTRX.append(Var)
            ES_MRTX.append(ES)
            
        
        VaR_c,ES,VaR_Unc = self.Indexation_of_VaR_CvaR(returns,sampled_garch_number_needed,Var_MTRX,ES_MRTX,Constant_VaR,J)
        
        return VaR_c,ES,VaR_Unc
    
    def Indexation_of_VaR_CvaR(self,returns,sampled_garch_number_needed,Var_MTRX,ES_MRTX,VaR_unc,J):
        
        l=0
        m=[]
        for x in range(int(round(len(returns.dropna().iloc[sampled_garch_number_needed:])/2,0))):
            idx=J.iloc[len(returns.dropna().iloc[:sampled_garch_number_needed])+l:,0].index[0]
            m.append(idx)
            l=l+2
            
        VaR_unc=pd.DataFrame(VaR_unc)
        VaR_unc.index=m
        
        VaR=pd.DataFrame(Var_MTRX)
        VaR.index=m
        
        ES=pd.DataFrame(ES_MRTX)
        ES.index=m
        
        VaR.columns = ['VaR t-student Garch 5%']
        ES.columns = ['CVaR t-student Garch 5%']
        VaR_unc.columns = ['VaR t-student 5%']
        return VaR,ES,VaR_unc
    
    def DD(self,returns):
        cum = (1+returns.dropna()).cumprod()
        DD = (cum.div(cum.cummax())-1)*100
        DD.columns = ['Drawdowns(in %)']
        return DD      
    
    def Risky_asset(self,ticker):
        df=pd.DataFrame()
        df=wb.DataReader(ticker,'yahoo', start='1995-01-01')['Adj Close']
        idx_b = df.index[0]
        df = df.resample('1W').last().pct_change().dropna()
        df = pd.DataFrame(df)
        df.columns = [ticker]
        return df,idx_b
    
    def Risky_free_asset(self,a):
        rf = quandl.get("USTREASURY/YIELD", authtoken="bBxaD71sAGrij1mxHsys")['1 YR']
        rf = rf.loc[a:].resample('1W').last()[1:]/100
        rf = pd.DataFrame(rf)
        return rf
    
    def jensen_alpha_beta(self,returns ,breturns,days):
        breturns = sm.add_constant(breturns)
        model = sm.OLS(returns[1:],breturns[1:]).fit()
        Beta = model.params[1]
        alpha_jensen = model.params[0] * days
        return Beta,alpha_jensen
        

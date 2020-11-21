import pandas as pd
from pandas_datareader import data as wb
import numpy as np
import quandl
from pandas import ExcelWriter
import matplotlib.pyplot as plt
from arch import arch_model
from scipy.stats import t
from statsmodels.distributions.empirical_distribution import ECDF
from scipy import stats as scipy_stats
import statsmodels.api as sm
rf = quandl.get("USTREASURY/YIELD")['1 YR']
rf = rf.loc['1995-01-01':].resample('1W').last()[1:]/100
rf = pd.DataFrame(rf)

while True :
    user = input("Please enter a new command('help' for a summary of the commands): ")
    # guide him
    if user == "help":
        print("=" * 90 + "\nTo visualize a TPPI strategy using SP500 etf(SPY) type 1:\n"
              + "=" * 90 +"\nTo register a TPPI strategy Backtest using SP500 etf(SPY) on excel type 2:\n"
              +"=" * 90+"\nto leave the app, simply type 'exit'\n\n")

    elif user =="1": 
        print("Choose your risky asset :")
        
        ticker = str(input())
        
        Risk_ass,idx = Initializing_values().Risky_asset(ticker)
        
        rfree = Initializing_values().Risky_free_asset(idx)
        
        print("Choose a Lock in")
        
        Lock_in = float(input())
        
        print("Choose a multiplier")
        
        m = float(input())
        
        print("Choose a floor")
        
        floor_percent = float(input())
        
        print("Choose a minimum risk capital rate to allocate ")
        
        Min_risk_part = float(input())
        
        print("Choose a Capital reinjection threshold ")
        
        Capital_reinjection_rate = float(input())
        
        print("Choose an amount to allocate")
        
        tipp = float(input())
        
        TIPP_values, floor_values,Capital_reinjection,reference_cap = Initializing_values().Values(Risk_ass,rfree,Lock_in,Min_risk_part,Capital_reinjection_rate,tipp,floor_percent,m)
        
        returns = TIPP_values.pct_change()
        #Initializing_values().Charted(sp500,CPPI_values, floor_values,Capital_reinjection,reference_cap)
        
        Omega_r = Initializing_values().Omega_ratio(returns)
        
        Sharp_ratio =  Initializing_values().Sharp_rt(returns,rfree,days=52)
        
        Sortino_ratio =  Initializing_values().Sortino_rt(returns,rfree,days=52)
        
        information_ratio =  Initializing_values().information_ratio(returns,Risk_ass,days=52)
        
        M2_Ratio =  Initializing_values().modigliani_ratio(returns,Risk_ass,rfree,days=52)
        
        PSR =  Initializing_values().probabilistic_sharpe_ratio(returns,Risk_ass,rfree,days=52)
        
        STD = Initializing_values().STD(returns,days=52)
        
        CGR = Initializing_values().CAGR(returns)
        
        Actualized_Var,Actualized_Expected_Shortfall,Cst_VaR =  Initializing_values().VaR_Studen_Distribution(returns,theta=0.05,sampled_garch_number_needed=500)
        
        Beta,jensen_alpha= Initializing_values().jensen_alpha_beta(returns ,Risk_ass,days=52)
        
        Max_Drawdown = Initializing_values().DD(returns).min()[0]
        
        cumulative_returns = Initializing_values().Cumulative_r(returns)
        
        print('Sharpe Ratio :',Sharp_ratio)
        
        print('--'*10)
        
        print('Sortino Ratio :',Sortino_ratio)
        
        print('--'*10)
        
        print('Information Ratio :',information_ratio)
        
        print('--'*10)
        
        print('Modigliani Ratio :',M2_Ratio)
        
        print('--'*10)
        
        print('Probabilistic Sharpe ratio (in %) :',PSR*100)
        
        print('--'*10)
        
        print('CAGR (in %) :',CGR*100)
        
        print('--'*10)
        
        print('Standard Deviation :',STD)
        
        print('--'*10)
        
        print('Conditional t-student Garch VaR 95%(in %):',Actualized_Var.iloc[-1,0])
        
        print('--'*10)
        
        print('Conditional t-student Garch CVaR 95%(in %):',Actualized_Expected_Shortfall.iloc[-1,0])
        
        print('--'*10)
        
        print('Unconditional VaR 95%(in %) :',Cst_VaR.iloc[-1,0])
        
        print('--'*10)
        
        print('Beta :',Beta)
        
        print('--'*10)
        
        print('Jensen alpha :',jensen_alpha)
        
        print('--'*10)
        
        print('Omega Ratio :',Omega_r)
        
        print('--'*10)
        
        print('Maximum Drawdown(in %) :',Max_Drawdown)
        
        print('--'*10)
        
        print('Cumulative returns(in %):',cumulative_returns*100)
        
        
        Initializing_values().Charted(Risk_ass,TIPP_values, floor_values,Capital_reinjection,reference_cap,Actualized_Var,Actualized_Expected_Shortfall,Cst_VaR)
        
            
    elif user == "2":
        
        print("Choose your risky asset :")
        
        ticker = str(input())
        
        Risk_ass,idx = Initializing_values().Risky_asset(ticker)
        
        rfree = Initializing_values().Risky_free_asset(idx)
        
        print("Choose a Lock in")
        
        Lock_in = float(input())
        
        print("Choose a multiplier")
        
        m = float(input())
        
        print("Choose a floor")
        
        floor_percent = float(input())
        
        print("Choose a minimum risk capital rate to allocate ")
        
        Min_risk_part = float(input())
        
        print("Choose a Capital reinjection rate ")
        
        Capital_reinjection_rate = float(input())
        
        print("Choose an amount to allocate(in M$)")
        
        tipp = float(input())
        
        TIPP_values, floor_values,Capital_reinjection,reference_cap = Initializing_values().Values(Risk_ass,rfree,Lock_in,Min_risk_part,Capital_reinjection_rate,tipp,floor_percent,m)
        
        print("The document will be registered on excel.Please wait for the confirmation")
        
        Initializing_values().Rgstr(Risk_ass,TIPP_values, floor_values,Capital_reinjection,reference_cap,rfree,52,0.05,500)
        
    elif user == "exit":
    
        print("\t\t Sucess you are out")
        
        break
            
    else:
    
        print('You typed on a wrong command.Please retry')  
    

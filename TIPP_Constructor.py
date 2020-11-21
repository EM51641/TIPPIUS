class TIPP:
    
    def __init__(self,returns,safe_asset_rate,Lock_in,Min_risk_part,Capital_reinjection_rate,cppi,floor_percent,m):
            self.returns = returns
            self.safe_asset_rate = safe_asset_rate
            self.Lock_in = Lock_in
            self.Min_risk_part = Min_risk_part
            self.Capital_reinjection_rate = Capital_reinjection_rate
            self.cppi = cppi
            self.floor_percent = floor_percent
            self.m = m
            self.tppi = self.tipp(returns,safe_asset_rate,Lock_in,Min_risk_part,Capital_reinjection_rate,cppi,floor_percent,m)
            
    def tipp(self,returns,safe_asset_rate,Lock_in,Min_risk_part,Capital_reinjection_rate,cppi,floor_percent,m):
        
        goal = len(returns.index)/52
        safe_assets = pd.DataFrame().reindex_like(returns)
        Year_rf = safe_asset_rate
        safe_assets[:] = safe_asset_rate / 52
        #Initial portfolio value
        CPPI = cppi
        # This is the minimum value I want to preserve
        F = CPPI * floor_percent/((1+Year_rf.iloc[0,0])**goal)
        Reference_cap = CPPI
        CPPI_values = pd.DataFrame().reindex_like(returns)
        floor_values = pd.DataFrame().reindex_like(returns)
        reference_cap = pd.DataFrame().reindex_like(returns)
        Capital_reinjection = pd.DataFrame().reindex_like(returns)
        floor_values[:] = F
        CPPI_max = CPPI
        for i in range(len(returns.index)):
            if CPPI > (1+Lock_in)*Reference_cap:
                Reference_cap = CPPI
                reference_cap.iloc[i] = CPPI
            else :
                reference_cap.iloc[i] = Reference_cap
            
            F_updated = CPPI * floor_percent/((1+Year_rf.iloc[i,0])**(goal))  #CPPI * floor_percent , Update floor Cap or no?
        
            if F < F_updated: # Floor Capital
                F = F_updated
            
            if CPPI<Reference_cap*Capital_reinjection_rate: #Capital Reinjection 
                Dif_CPPI_F = Reference_cap*Capital_reinjection_rate - CPPI
                Reference_cap = Reference_cap - Dif_CPPI_F
                reference_cap.iloc[i] = Reference_cap
                CPPI  = CPPI + Dif_CPPI_F 
                Capital_reinjection.iloc[i] = Dif_CPPI_F
            else : 
                Capital_reinjection.iloc[i] = 0
    
            
            C = CPPI - F
            risky_asset_e = max(min(m * C, CPPI),Min_risk_part*CPPI) 
            risklet_asset = CPPI - risky_asset_e
            CPPI = risky_asset_e * (1 + returns.iloc[i].item()) + risklet_asset * (1 + safe_assets.iloc[i].item())
            CPPI_values.iloc[i] = CPPI
            floor_values.iloc[i] = F
            goal = goal - 1/52
        CPPI_values.columns = ['TIPP Strategy']
        return CPPI_values, floor_values,Capital_reinjection,reference_cap 

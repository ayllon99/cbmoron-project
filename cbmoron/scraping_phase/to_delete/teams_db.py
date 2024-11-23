import pandas as pd


df=pd.read_pickle('results_LEB_ORO.pkl')
away=df[['away_id_team','away_team_name']]
away.columns=['home_id_team','home_team_name']
done=pd.concat([df[['home_id_team','home_team_name']],away],axis=0)
done.columns=['team_id','team_name']
done['team_name']=done['team_name'].apply(lambda x: x.strip())
done.drop_duplicates(inplace=True)
done.reset_index(drop=True,inplace=True)
#done.to_pickle('teams.pkl')

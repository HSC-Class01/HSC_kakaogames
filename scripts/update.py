"""OpenDART collector and financial ratio engine; no fabricated data."""
import os,json,time,datetime,requests,pathlib,io,zipfile,xml.etree.ElementTree as ET
ROOT=pathlib.Path(__file__).resolve().parents[1]; KEY=os.getenv('DART_API_KEY','').strip()
if not KEY: raise SystemExit('Missing DART_API_KEY GitHub Actions secret')
S=requests.Session(); BASE='https://opendart.fss.or.kr/api/'
def get(endpoint,params):
 for attempt in range(4):
  try:
   r=S.get(BASE+endpoint,params={'crtfc_key':KEY,**params},timeout=45);r.raise_for_status();j=r.json()
   if j.get('status')=='013':return None
   if j.get('status')!='000':raise RuntimeError(f'{endpoint}: {j.get("status")} {j.get("message")}')
   return j
  except requests.RequestException:
   if attempt==3:raise
   time.sleep(2**attempt)
def number(v):
 try:return int(str(v).replace(',','').strip())
 except (TypeError,ValueError):return None
def divide(a,b,pct=False):
 if a is None or b in (None,0):return None
 return round(a/b*(100 if pct else 1),3)
def main():
 r=S.get(BASE+'corpCode.xml',params={'crtfc_key':KEY},timeout=90);r.raise_for_status()
 with zipfile.ZipFile(io.BytesIO(r.content)) as z:root=ET.fromstring(z.read('CORPCODE.xml'))
 corp=next((e.findtext('corp_code') for e in root.findall('list') if e.findtext('stock_code')=='293490'),None)
 if not corp:raise RuntimeError('Kakao Games corporation code not found')
 raw=ROOT/'data/raw';raw.mkdir(parents=True,exist_ok=True);records=[]
 specs={
 'revenue':('IS',['ifrs-full_Revenue','ifrs_Revenue','ifrs-full_RevenueFromContractsWithCustomers'],['매출액','영업수익']),
 'cost_of_sales':('IS',['ifrs-full_CostOfSales','ifrs_CostOfSales'],['매출원가']),
 'gross_profit':('IS',['ifrs-full_GrossProfit','ifrs_GrossProfit'],['매출총이익']),
 'sga':('IS',['dart_TotalSellingGeneralAdministrativeExpenses'],['판매비와관리비']),
 'operating_income':('IS',['dart_OperatingIncomeLoss'],['영업이익(손실)','영업이익']),
 'pretax_income':('IS',['ifrs-full_ProfitLossBeforeTax','ifrs_ProfitLossBeforeTax'],['법인세비용차감전순이익(손실)','법인세비용차감전순이익']),
 'net_income':('IS',['ifrs-full_ProfitLoss','ifrs_ProfitLoss'],['당기순이익(손실)','당기순이익']),
 'parent_income':('IS',['ifrs-full_ProfitLossAttributableToOwnersOfParent','ifrs_ProfitLossAttributableToOwnersOfParent'],['지배기업의 소유주에게 귀속되는 당기순이익']),
 'assets':('BS',['ifrs-full_Assets','ifrs_Assets'],['자산총계']),
 'liabilities':('BS',['ifrs-full_Liabilities','ifrs_Liabilities'],['부채총계']),
 'equity':('BS',['ifrs-full_Equity','ifrs_Equity'],['자본총계']),
 'parent_equity':('BS',['ifrs-full_EquityAttributableToOwnersOfParent','ifrs_EquityAttributableToOwnersOfParent'],['지배기업의 소유주에게 귀속되는 자본']),
 'cash':('BS',['ifrs-full_CashAndCashEquivalents','ifrs_CashAndCashEquivalents'],['현금및현금성자산']),
 'receivables':('BS',['ifrs-full_TradeAndOtherCurrentReceivables','ifrs_TradeAndOtherCurrentReceivables'],['매출채권','매출채권 및 기타유동채권']),
 'inventory':('BS',['ifrs-full_Inventories','ifrs_Inventories'],['재고자산']),
 'ppe':('BS',['ifrs-full_PropertyPlantAndEquipment','ifrs_PropertyPlantAndEquipment'],['유형자산']),
 'current_assets':('BS',['ifrs-full_CurrentAssets','ifrs_CurrentAssets'],['유동자산']),
 'current_liabilities':('BS',['ifrs-full_CurrentLiabilities','ifrs_CurrentLiabilities'],['유동부채']),
 'trade_payables':('BS',['ifrs-full_TradeAndOtherCurrentPayables','ifrs_TradeAndOtherCurrentPayables'],['매입채무','매입채무 및 기타유동채무']),
 'short_borrowings':('BS',['ifrs-full_ShorttermBorrowings','ifrs_ShorttermBorrowings','dart_ShortTermBorrowings'],['단기차입금']),
 'long_borrowings':('BS',['ifrs-full_LongtermBorrowings','ifrs_LongtermBorrowings','dart_LongTermBorrowingsGross'],['장기차입금']),
 'operating_cash_flow':('CF',['ifrs-full_CashFlowsFromUsedInOperatingActivities','ifrs_CashFlowsFromUsedInOperatingActivities'],['영업활동현금흐름']),
 'investing_cash_flow':('CF',['ifrs-full_CashFlowsFromUsedInInvestingActivities','ifrs_CashFlowsFromUsedInInvestingActivities'],['투자활동현금흐름']),
 'financing_cash_flow':('CF',['ifrs-full_CashFlowsFromUsedInFinancingActivities','ifrs_CashFlowsFromUsedInFinancingActivities'],['재무활동현금흐름']),
 'purchase_ppe':('CF',['ifrs-full_PurchaseOfPropertyPlantAndEquipment','ifrs_PurchaseOfPropertyPlantAndEquipment'],['유형자산의 취득']),
 'purchase_intangibles':('CF',['ifrs-full_PurchaseOfIntangibleAssets','ifrs_PurchaseOfIntangibleAssets'],['무형자산의 취득']),
 'interest_expense':('IS',['ifrs-full_FinanceCosts','ifrs_FinanceCosts'],['이자비용']),
 }
 now=datetime.date.today()
 for year in range(2010,now.year+1):
  for code,period in [('11013','Q1'),('11012','H1'),('11014','Q3'),('11011','FY')]:
   data=get('fnlttSinglAcntAll.json',{'corp_code':corp,'bsns_year':year,'reprt_code':code,'fs_div':'CFS'});scope='CFS'
   if data is None:data=get('fnlttSinglAcntAll.json',{'corp_code':corp,'bsns_year':year,'reprt_code':code,'fs_div':'OFS'});scope='OFS'
   if data is None:continue
   items=data.get('list',[])
   (raw/f'{year}_{period}.json').write_text(json.dumps({'scope':scope,'items':items},ensure_ascii=False,indent=2),encoding='utf-8')
   def find(spec):
    sj,ids,names=spec
    for typ,values in [('account_id',ids),('account_nm',names)]:
     for v in values:
      matches=[x for x in items if x.get('sj_div')==sj and x.get(typ)==v and x.get('account_detail','-') in ('-','')]
      for x in matches:
       n=number(x.get('thstrm_amount'))
       if n is not None:return n
    return None
   row={'year':year,'period':period,'scope':scope,'cumulative':period!='FY'}
   row.update({key:find(spec) for key,spec in specs.items()})
   if row['gross_profit'] is None and row['revenue'] is not None and row['cost_of_sales'] is not None:row['gross_profit']=row['revenue']-row['cost_of_sales']
   capex_parts=[v for v in (row['purchase_ppe'],row['purchase_intangibles']) if v is not None]
   row['capex']=sum(capex_parts) if capex_parts else None
   row['fcf']=row['operating_cash_flow']-row['capex'] if None not in (row['operating_cash_flow'],row['capex']) else None
   debt_parts=[v for v in (row['short_borrowings'],row['long_borrowings']) if v is not None]
   row['interest_bearing_debt']=sum(debt_parts) if debt_parts else None
   row['net_debt']=row['interest_bearing_debt']-row['cash'] if None not in (row['interest_bearing_debt'],row['cash']) else None
   for target,num,den in [('gross_margin','gross_profit','revenue'),('operating_margin','operating_income','revenue'),('net_margin','net_income','revenue'),('current_ratio','current_assets','current_liabilities'),('debt_ratio','liabilities','equity'),('equity_ratio','equity','assets'),('borrowing_dependence','interest_bearing_debt','assets')]:
    row[target]=divide(row[num],row[den],True) if den!='equity' or row['equity'] is not None and row['equity']>0 else None
   row['quick_ratio']=divide(row['current_assets']-row['inventory'],row['current_liabilities'],True) if None not in (row['current_assets'],row['inventory']) else None
   row['interest_coverage']=divide(row['operating_income'],row['interest_expense']) if row['interest_expense'] is not None and row['interest_expense']>0 else None
   row['cfo_to_income']=divide(row['operating_cash_flow'],row['net_income'])
   records.append(row);print(year,period,scope,flush=True)
   time.sleep(.08)
 # Comparable periods only; use prior-year closing balance for annual, prior FY for interim.
 by={(r['year'],r['period'],r['scope']):r for r in records}
 for r in records:
  previous=by.get((r['year']-1,'FY',r['scope']))
  for output,flow,balance in [('roa','net_income','assets'),('roe','parent_income' if r['parent_income'] is not None and r['parent_equity'] is not None else 'net_income','parent_equity' if r['parent_income'] is not None and r['parent_equity'] is not None else 'equity'),('asset_turnover','revenue','assets')]:
   base=r[balance];old=previous[balance] if previous else None
   avg=(base+old)/2 if base is not None and old is not None and base+old>0 else None
   factor={'Q1':4,'H1':2,'Q3':4/3,'FY':1}[r['period']]
   r[output]=divide(r[flow]*factor if r[flow] is not None else None,avg,output!='asset_turnover')
  prev_same=by.get((r['year']-1,r['period'],r['scope']))
  r['revenue_growth']=divide((r['revenue']-prev_same['revenue'])*100,prev_same['revenue']) if prev_same and r['revenue'] is not None and prev_same['revenue'] is not None and prev_same['revenue']>0 else None
  r['receivables_days']=divide((r['receivables']+(previous['receivables'] if previous else None))/2*365, r['revenue']*{'Q1':4,'H1':2,'Q3':4/3,'FY':1}[r['period']]) if previous and r['receivables'] is not None and previous['receivables'] is not None and r['revenue'] is not None else None
  r['inventory_days']=divide((r['inventory']+previous['inventory'])/2*365,r['cost_of_sales']*{'Q1':4,'H1':2,'Q3':4/3,'FY':1}[r['period']]) if previous and r['inventory'] is not None and previous['inventory'] is not None and r['cost_of_sales'] is not None else None
  # DPO needs purchases on credit, not simply cost of sales. Do not fabricate.
  r['dpo']=None;r['ccc']=None;r['ebitda']=None;r['ebitda_margin']=None;r['roic']=None;r['net_debt_to_ebitda']=None;r['per']=None;r['pbr']=None;r['ev_to_ebitda']=None;r['fcf_yield']=None
 out=ROOT/'data/processed';out.mkdir(parents=True,exist_ok=True)
 (out/'financials.json').write_text(json.dumps({'updated_at':now.isoformat(),'company':'카카오게임즈','stock_code':'293490','records':records,'notes':['누적 분기 손익 및 현금흐름 수치','연결 우선/별도 대체, 서로 다른 기준 간 비교 제외','ROA/ROE/회전율: 전년말과 당기말 평균잔액 사용 및 연환산 참고치','EBITDA, ROIC, DPO, CCC 및 시장가치 지표는 신뢰 가능한 원천 부족 시 결측']},ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__':main()

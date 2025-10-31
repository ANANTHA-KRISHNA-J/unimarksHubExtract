from dotenv import load_dotenv
import os
from langchain.tools import tool
from pydantic import BaseModel, Field
import datetime, requests
import pandas as pd
import streamlit as st
import datetime
import json

reversepocmaps = {
  "76821774": "Priyadharshini",
  "76821788": "Sandhiya Durai",
  "76821797": "Lavanya Vasu",

  "680448818": "Sachin Priya Daniel S",
  "714526095": "Shunmuga Priya",
  
  "78470503": "Madesh Krishna",  "408847625": "Samuel J",
  "522462019": "Ananthi N",
  "78471123": "Hariprasad K",  "523812380": "Mohan M",

  "86718745": "Sandhiya Durai",
  "149025425": "Admin Pearlpick",
  "149053803": "Kamini B",
  
  "149055031": "Mansoor ali",
  "149055768": "Suresh Kumar",
  "149747514": "Ajay s",
  "149749362": "Arul A",  "153245866": "Dinesh Kumar",
  "150407859": "Tharani Ravi",
  "523817838": "Raj Kamal",
  "78642521": "Lenin Samuel",

  "154662495": "Support Unimarks",
  "159668346": "Legal Intern",
  "159721290": "Sree Ramya Vangala",
  "159759344": "Naseema A",
  "171398516": "Pearlpick Ventures V",  "206374727": "Kavitha Sagayaraj",
  "230919210": "Mohammed Tajuddin",  "78469530": "Lavanya Vasu","78469938": "Priya dharshini",


  "245151011": "Mohitha CS",
  "257629073": "Jigar k Patel",
  "279925039": "Siva Kumar",
  "374660102": "Dinesh R",
  "398321190": "Leads Pearlpick Ventures",
  "523812209": "dinesh 1",
  "565519544": "Vaishali J",
  "601770628": "Sophia Jeyakar",  "79184854": "Mary Santo Disha",  "150046306": "Viswesswaar P",
  "150057355": "Divya S",
  "79299552": "Bhavani Sri",  "150484830": "Amanullah Sulthan",  "180329123": "Vijaya Lakshmi",
  "636134420": "Oveya S", "77492250": "Ankith Kumar","78470076": "Ashwini M","149055026": "Ajith Prathap Singh",
  
}
load_dotenv()
hub_token = os.getenv('HUBSPOT_API_KEY')
closed_stages = ["closedwon", "14459000", "14440564"]

class Applyfilters(BaseModel):
    """Inputs to fetching deals across multuple fields like date range, Deal types, deal Stage, Deal owner, Amount."""
    start_date: str = Field(..., description="Start date (YYYY-MM-DD)")
    end_date: str = Field(..., description="End date (YYYY-MM-DD)")
    dealtypes : list[str] | None = Field(default=None,description="Optional list of dealTypes to be filtered with")
    dealstages : list[str] | None = Field(default=None,description="Optional list of dealStages to be filtered with")
    pocfilters : list[str] | None = Field(default=None,description="Optional list of POC names to be filtered with")
@tool(args_schema=Applyfilters)
def fetch_deals(start_date: str, end_date: str, dealtypes:list[str] | None = None , dealstages:list[str]| None=None, pocfilters:list[str]|None=None):
    """Fetch closed HubSpot deals with filters like start_date,end_date, dealtypes ,Dealstages"""
    try:
        dt_start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        dt_end = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        # Convert to HubSpot ISO8601 format
        #start_str = dt_start.strftime("%Y-%m-%dT%H:%M:%SZ")
        #end_str = dt_end.strftime("%Y-%m-%dT%H:%M:%SZ")

        url = "https://api.hubapi.com/crm/v3/objects/deals/search"
        headers = {"Authorization": f"Bearer {hub_token}"}
        all_deals, after = [], None
        while True:
            payload = {
                "limit": 100,
                "properties": [
                    "dealname", "amount", "dealstage", "hubspot_owner_id",
                    "closedate", "dealtype", "deal_channel", "service_s__name"
                ],
                "filterGroups": [{
                    "filters": [
                        {"propertyName": "closedate", "operator": "GTE", "value": start_date},
                        {"propertyName": "closedate", "operator": "LTE", "value": end_date},
                        #{"propertyName": "dealstage", "operator": "IN", "values": closed_stages},
                    ]
                }]
            }
            if dealtypes:
                if len(dealtypes)>1:
                    payload['filterGroups'][0]['filters'].append({"propertyName": "dealtype", "operator": "IN", "values": dealtypes})
                else:
                    payload['filterGroups'][0]['filters'].append({"propertyName": "dealtype", "operator": "EQ", "value": str(dealtypes[0])})

            if dealstages:
                if len(dealstages)>1:
                    payload['filterGroups'][0]['filters'].append({"propertyName": "dealstage", "operator": "IN", "values": dealstages})
                elif len(dealstages)==1:
                    payload['filterGroups'][0]['filters'].append({"propertyName": "dealstage", "operator": "EQ", "value": dealstages[0]})
                else:
                    payload['filterGroups'][0]['filters'].append({"propertyName": "dealstage", "operator": "IN", "values": closed_stages})
            if pocfilters:
                if len(pocfilters) > 1:
                    payload['filterGroups'][0]['filters'].append({
                        "propertyName": "hubspot_owner_id",
                        "operator": "IN",
                        "values": pocfilters
                    })
                else:
                    payload['filterGroups'][0]['filters'].append({
                        "propertyName": "hubspot_owner_id",
                        "operator": "EQ",
                        "value": pocfilters[0]
                    })

            if after:
                payload["after"] = after

            response = requests.post(url, headers=headers, json=payload)
            if response.status_code != 200:
                return st.error(response.text)

            data = response.json()
            all_deals.extend(data.get("results", []))
            after = data.get("paging", {}).get("next", {}).get("after")
            if not after:
                break

        return len(all_deals) , all_deals

    except Exception as e:
        return {st.error(type(e).__name__):st.error({str(e)})}

# def dict_to_table(data):
#     df = pd.json_normalize(data, sep="_")
#     return st.dataframe(df) 

# with open('ownersmap.json','r') as f:
#     owners=json.load(f)
reversestagemaps = {
    'Qualified': 'qualifiedtobuy',
    'Proposal Sent': 'contractsent',
    'In Progress': 'decisionmakerboughtin',
    'Awaiting Payment': '14261535',
    'Payment Processed': '14440564',
    'Closed won': 'closedwon',
    'Closed lost': 'closedlost',
    'Sent to Ops': '14459000',
    'New': 'appointmentscheduled',
    'Negotiation': '14261534'
}
# with open("stagesmap.json", "r") as f:
#     stages = json.load(f)

#stagemap = {"closedwon":"Closed won","14440564":"Payment Processed","14459000":"Sent to Ops"}
typemap = {'newbusiness':'New Business','existingbusiness':'Existing Business','New Affiliate':'New Affiliate','Existing Affiliate':'Existing Affiliate'}
stage_display_map = {v: k for k, v in reversestagemaps.items()}


def dict_to_table(data):
    df = pd.json_normalize(data, sep="_")
    if df.empty:
        st.warning("No deals found for selected filters.")
        return pd.DataFrame()
    df = df.rename(columns={'id':'Deal ID','createdAt':'Create Date',"properties_dealstage": "Deal Stages",
                            'updatedAt':'Updated At','properties_amount':'Amount','properties_closedate':'Closed Date','properties_createdate':'Create Date1',
                            'properties_dealname':'Deal Name','properties_deal_channel':'Deal Channel','properties_hubspot_owner_id':'POC','properties_service_s__name':'Service Done',
                            'properties_dealtype':'Deal Type','properties_hs_lastmodifieddate':'Last Modified','properties_hs_object_id':'Object ID','properties_pipeline':'Pipeline'})
    df = df.drop(columns=['Create Date1','archived','Last Modified','Object ID'],errors='ignore')
    #df['Deal Stages']= df['Deal Stages'].map(stages) 
    df['Deal Type']= df['Deal Type'].map(typemap).fillna(df['Deal Type'])
    df['Deal Stages'] = df['Deal Stages'].map(stage_display_map).fillna(df['Deal Stages'])
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce').fillna(0)
    df['POC'] = df['POC'].map(reversepocmaps).fillna(df['POC'])
    if "url" in df.columns:
        df = df.drop(columns=["url"])



    
    return df
    

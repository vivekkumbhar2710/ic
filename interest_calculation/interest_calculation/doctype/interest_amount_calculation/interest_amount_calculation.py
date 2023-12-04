# Copyright (c) 2023, Abhishek Chougule and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta

class InterestAmountCalculation(Document):
	@frappe.whitelist() 
	def get_BalanceDetails(self):
		todate=self.to_date
		fromdate=self.from_date
		date_format = "%Y-%m-%d"
		start_date = datetime.strptime(str(fromdate), date_format)
		end_date = datetime.strptime(str(todate), date_format)
		if start_date <= end_date:
			self.append("interest_rate_details",
									{
										"from_date": self.from_date,
										"to_date":self.to_date,
									},)
		while start_date <= end_date:
			self.append("interest_calculation_details",
								{
									"date": start_date.strftime(date_format),
								},)
			start_date += timedelta(days=1)
		

	@frappe.whitelist() 
	def get_Details(self):
		lst=[]
		balance=0
		self.total_interest=0
		for i in self.get('interest_calculation_details'):
			for j in self.get('interest_rate_details'):
				if i.date>=j.from_date and i.date<=j.to_date:
					i.interest_rate=j.interest_rate
					# ac=frappe.db.get_list("Account",fields=['name','root_type'],filters={'name':self.select_account})
					# for l in ac:
					creditpe=frappe.db.get_list("Payment Entry",fields=["name","paid_amount","paid_from","paid_to","paid_from_account_balance","paid_to_account_balance","posting_date"],filters={'paid_from':self.select_account,'posting_date':i.date},limit=1)
					if creditpe:
						for k in creditpe:
							tdate=k.posting_date
							i.credit=k.paid_amount
							i.balance=k.paid_from_account_balance-k.paid_amount #if l.root_type=='Asset' else k.paid_from_account_balance+k.paid_amount
						
					
					debitpe=frappe.db.get_list("Payment Entry",fields=["name","paid_amount","paid_from","paid_to","paid_from_account_balance","paid_to_account_balance","posting_date"],filters={'paid_to':self.select_account,'posting_date':i.date},limit=1)
					if debitpe:
						for k in debitpe:
							tdate=k.posting_date
							i.debit=k.paid_amount
							i.balance=k.paid_to_account_balance+k.paid_amount #if l.root_type=='Asset' else k.paid_to_account_balance-k.paid_amount
					
					lst.append(i.balance)
					if i.credit==0 and i.debit==0:
						if len(lst)<2:
							balance=lst[-1]
						else:
							i.balance=lst[-2]

			if i.credit==0 and i.debit==0:			
				pass
			else:
				balance=i.balance
		for i in self.get('interest_calculation_details'):
			if i.credit==0 and i.debit==0 and i.date>=str(tdate):
				i.balance=balance
			i.interest_amount=(i.interest_rate*i.balance)/36500
			
		for i in self.get('interest_calculation_details'):

			self.total_interest=self.total_interest+i.interest_amount
			
			

		




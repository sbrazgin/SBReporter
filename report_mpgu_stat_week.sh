# copy excel file
varDate=`date +%d_%m_%Y`
varFileName="report_mpgu_stat_week_1_${varDate}.xlsx"
cp report_mpgu_stat_week.xlsx $varFileName

# add data to excel
alias python=/opt/Python/Python-3.6.5/python
./SBReporter.py -i report_MPGU_1_week.ini -o ${varFileName}

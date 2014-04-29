# Sorry but for now we need this cleanup script because gunicorn doesn't have an
# on_exit hook to cleanup what the application need to run.
# So you should run this script to cleanup all the iptable rules the application
# created during its runtime. Please notice that the database will persist!

from iptables import IPTables
ipt = IPTables()
ipt.shutdown()

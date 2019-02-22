import ns.applications
import ns.core
import ns.internet
import ns.network
import ns.point_to_point
import ns.stats
import sys


# Parameters
packetSize = 256
applicationDataRate = "50kbps"

# Create nodes
nodes = ns.network.NodeContainer()
nodes.Create(3)

nodeAB = ns.network.NodeContainer()
nodeAB.Add(nodes.Get(0))
nodeAB.Add(nodes.Get(1))
nodeBC = ns.network.NodeContainer()
nodeBC.Add(nodes.Get(1))
nodeBC.Add(nodes.Get(2))



# Helper class used to generate links
pointToPoint = ns.point_to_point.PointToPointHelper()
pointToPoint.SetDeviceAttribute("DataRate", ns.core.StringValue("1Mbps"))
pointToPoint.SetChannelAttribute("Delay", ns.core.StringValue("10ms"))

# Generate links 
linkAB = pointToPoint.Install(nodeAB)
linkBC = pointToPoint.Install(nodeBC)


# Load Internet stack into nodes
stack = ns.internet.InternetStackHelper()
#stack.SetRoutingHelper(listRouting)
stack.Install(nodes)

# Use IPv4 address helper to configure IPv4 addresses and set the metrics (costs) of the links
ipv4 = ns.internet.Ipv4AddressHelper()
ipv4.SetBase(ns.network.Ipv4Address("10.1.1.0"),
                ns.network.Ipv4Mask("255.255.255.0"))
interfaceAB = ipv4.Assign(linkAB)
interfaceAB.SetMetric(0,2)
interfaceAB.SetMetric(1,2)
ipv4.SetBase(ns.network.Ipv4Address("10.1.2.0"),
                ns.network.Ipv4Mask("255.255.255.0"))
interfaceBC = ipv4.Assign(linkBC)
interfaceBC.SetMetric(0,2)
interfaceBC.SetMetric(1,2)


# Generate global routing table after setting up the network
ns.internet.Ipv4GlobalRoutingHelper.PopulateRoutingTables()


ascii = ns.network.AsciiTraceHelper()
output = ascii.CreateFileStream("RoutingTable")
ns.internet.Ipv4GlobalRoutingHelper.PrintRoutingTableAllAt(ns.core.Seconds(2.0), output)


UDPport = 9
UDPsink = ns.applications.PacketSinkHelper("ns3::UdpSocketFactory", 
  ns.network.InetSocketAddress(ns.network.Ipv4Address.GetAny(),UDPport))
sourceNode = ns.network.NodeContainer(nodes.Get (0))
sinkNode = ns.network.NodeContainer(nodes.Get (2))

App = UDPsink.Install(sinkNode)
App.Start(ns.core.Seconds(0.0))
App.Stop(ns.core.Seconds(10.0))

sinkSocketAddress = ns.network.InetSocketAddress(interfaceBC.GetAddress(1), UDPport)
UDPsource = ns.applications.OnOffHelper("ns3::UdpSocketFactory", sinkSocketAddress)
UDPsource.SetAttribute("OnTime", ns.core.StringValue("ns3::ConstantRandomVariable[Constant=1]"));
UDPsource.SetAttribute("OffTime", ns.core.StringValue("ns3::ConstantRandomVariable[Constant=0]"));
UDPsource.SetAttribute("PacketSize", ns.core.UintegerValue(packetSize))
UDPsource.SetAttribute("DataRate", ns.core.StringValue(applicationDataRate))
App = UDPsource.Install(sourceNode)
App.Start(ns.core.Seconds(1.0))
App.Stop(ns.core.Seconds(10.0))



# Set probe for data collection. Note that tracePath determines what data we are collecting, "*" is 
# the wildcard notation, here it means that collecting data from any node on the NodeList. You may 
# exchange "*" with the node number in order to collect for only one node.
probeType = "ns3::Ipv4PacketProbe"
tracePath = "/NodeList/*/$ns3::Ipv4L3Protocol/Rx"

# Use GnuplotHelper to plot the packet byte count over time
plotHelper = ns.stats.GnuplotHelper()

# Configure the plot.  The first argument is the file name prefix for the output files generated.  
# The second, third, and fourth arguments are, respectively, the plot title, x-axis, and y-axis labels
plotHelper.ConfigurePlot ("ece158b-second-byte-count", "Packet Byte Count vs. Time", 
  "Time (Seconds)", "Packet Byte Count", "png")

# Specify the probe type, trace source path , and probe output trace source ("OutputBytes") to plot.  
# The fourth argument specifies the name of the data series label on the plot.  
# The last argument formats the plot by specifying where the key should be placed.
plotHelper.PlotProbe (probeType, tracePath, "OutputBytes", "Packet Byte Count", 
  ns.stats.GnuplotAggregator.KEY_BELOW)





# Set stop simulation event at time 10s
ns.core.Simulator.Stop(ns.core.Seconds(10.0))

# Start simulation
print("Starting simulation")
ns.core.Simulator.Run()

# Clean up after simulation ends
print("Simulation done")
ns.core.Simulator.Destroy()

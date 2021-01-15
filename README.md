# RL_LocalGravityAssistant
Rocket League modding tool, which assists in creating realistic gravity situations in custom maps

## How to install
1. Download this repository (either use git clone or download a zip file and extract it)
2. Run InstallDependencies.bat once. This will download some python packages.
3. Execute the mod with executeTool.bat

## How to use
The following components in UDK will be used:
- Trigger:     Represents a mass point. 
  - TAG:                  Defines the mass in kilograms
  - Collision Height:     Min distance (no effect within this range) 
  - Collision Radius:     Max distance (no effect afterwards)
- PathNode:    Is used to store the force direction for every ForceVolume. They must be placed and linked manually!
- ForceVolume: Used to apply Force on game objects. Place them, where the the custom gravity should take effect. 
  - ForceMode:            Will be overwritten.
  - Custom Force Dir.:    REQUIRES MANUAL ATTACHMENT. Each ForceVolume must have its own attached PathNode
### Modding workflow
1. Create the rough shape of your map with mass points in mind
2. Place a single ForceVolume and PathNode
3. Reference the PathNode from the ForceVolume; Group both components. (grouping is useful, not required)
4. Copy the group to wherever you need custom gravity
CAUTION: UDK will only handle about ~750 items at once during some steps.
Make sure, that your groupings are not bigger.
5. Place and configure your Trigger objects (your mass points)
6. Scelect all Triggers (i.e. Ctrl+A in the Scenes tab) and copy them to your clipboard
7. Start the script and press enter, indicating that you have copied the Triggers.
8. Copy a batch or all ForceVolumes with their PathNodes to your clipboard.
9. Press enter in the mod tool.
10. Delete your previously scelected items in UDK and paste your clipboard.
11. Press I then enter and jump to step 8 if you want to process further ForceVolumes
12. Press V if you want so see a visualization
13. PROFIT. Your ForceVolumes are now completely configured.

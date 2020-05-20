# ios-modular-example

Sample repository showing a solution for a simple dependency resolution to enhance usage of XcodeGen.

## Usage:
1. Build Carthage dependencies with `carthage bootstrap --platform ios`
2. Run `./setup.sh`. What it does is: 
⋅⋅* run `resolve-dependencies.py` script 
⋅⋅* run `xcodegen` with `project-resolved.yml` files produced by the script as input
3. Open `ModularApp.xcworkspace` and run the app

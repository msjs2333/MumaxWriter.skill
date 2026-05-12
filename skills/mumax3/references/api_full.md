# mumax3.12 API Full Reference

Source: generated from the official mumax3.12 API page, <https://mumax.github.io/api.html>, downloaded 2026-05-12.

Distribution decision for v0.1.0: keep this file as a sparse identifier/signature index with provenance. It is not a replacement for the official API documentation and should not be treated as authoritative for detailed semantics, examples, or version changes.

Use this file as an on-demand identifier/signature index when reviewing scripts or when `api_index.md` does not cover a requested API. It intentionally keeps prose sparse; check the official API page for detailed semantics, examples, and version changes.

Identifier names are case-insensitive in mumax3 scripts, but this index preserves the official spelling.

## Mesh size and geometry

- `SetCellSize(float64, float64, float64)`
- `SetGeom(Shape)`
- `SetGridSize(int, int, int)`
- `SetMesh(int, int, int, float64, float64, float64, int, int, int)`
- `SetPBC(int, int, int)`
- `EdgeSmooth`

## Shapes

- `Cell(int, int, int) Shape`
  - methods: `Add( Shape ) Intersect( Shape ) Inverse( ) Repeat( float64 float64 float64 ) RotX( float64 ) RotY( float64 ) RotZ( float64 ) Scale( float64 float64 float64 ) Sub( Shape ) Transl( float64 float64 float64 ) Xor( Shape )`
- `Circle(float64) Shape`
  - methods: `Add( Shape ) Intersect( Shape ) Inverse( ) Repeat( float64 float64 float64 ) RotX( float64 ) RotY( float64 ) RotZ( float64 ) Scale( float64 float64 float64 ) Sub( Shape ) Transl( float64 float64 float64 ) Xor( Shape )`
- `Cone(float64, float64) Shape`
  - methods: `Add( Shape ) Intersect( Shape ) Inverse( ) Repeat( float64 float64 float64 ) RotX( float64 ) RotY( float64 ) RotZ( float64 ) Scale( float64 float64 float64 ) Sub( Shape ) Transl( float64 float64 float64 ) Xor( Shape )`
- `Cuboid(float64, float64, float64) Shape`
  - methods: `Add( Shape ) Intersect( Shape ) Inverse( ) Repeat( float64 float64 float64 ) RotX( float64 ) RotY( float64 ) RotZ( float64 ) Scale( float64 float64 float64 ) Sub( Shape ) Transl( float64 float64 float64 ) Xor( Shape )`
- `Cylinder(float64, float64) Shape`
  - methods: `Add( Shape ) Intersect( Shape ) Inverse( ) Repeat( float64 float64 float64 ) RotX( float64 ) RotY( float64 ) RotZ( float64 ) Scale( float64 float64 float64 ) Sub( Shape ) Transl( float64 float64 float64 ) Xor( Shape )`
- `Ellipse(float64, float64) Shape`
  - methods: `Add( Shape ) Intersect( Shape ) Inverse( ) Repeat( float64 float64 float64 ) RotX( float64 ) RotY( float64 ) RotZ( float64 ) Scale( float64 float64 float64 ) Sub( Shape ) Transl( float64 float64 float64 ) Xor( Shape )`
- `Ellipsoid(float64, float64, float64) Shape`
  - methods: `Add( Shape ) Intersect( Shape ) Inverse( ) Repeat( float64 float64 float64 ) RotX( float64 ) RotY( float64 ) RotZ( float64 ) Scale( float64 float64 float64 ) Sub( Shape ) Transl( float64 float64 float64 ) Xor( Shape )`
- `GrainRoughness(float64, float64, float64, int) Shape`
  - methods: `Add( Shape ) Intersect( Shape ) Inverse( ) Repeat( float64 float64 float64 ) RotX( float64 ) RotY( float64 ) RotZ( float64 ) Scale( float64 float64 float64 ) Sub( Shape ) Transl( float64 float64 float64 ) Xor( Shape )`
- `ImageShape(string) Shape`
  - methods: `Add( Shape ) Intersect( Shape ) Inverse( ) Repeat( float64 float64 float64 ) RotX( float64 ) RotY( float64 ) RotZ( float64 ) Scale( float64 float64 float64 ) Sub( Shape ) Transl( float64 float64 float64 ) Xor( Shape )`
- `Layer(int) Shape`
  - methods: `Add( Shape ) Intersect( Shape ) Inverse( ) Repeat( float64 float64 float64 ) RotX( float64 ) RotY( float64 ) RotZ( float64 ) Scale( float64 float64 float64 ) Sub( Shape ) Transl( float64 float64 float64 ) Xor( Shape )`
- `Layers(int, int) Shape`
  - methods: `Add( Shape ) Intersect( Shape ) Inverse( ) Repeat( float64 float64 float64 ) RotX( float64 ) RotY( float64 ) RotZ( float64 ) Scale( float64 float64 float64 ) Sub( Shape ) Transl( float64 float64 float64 ) Xor( Shape )`
- `Line(float64, float64, float64, float64, float64, float64, float64, string) Shape`
  - methods: `Add( Shape ) Intersect( Shape ) Inverse( ) Repeat( float64 float64 float64 ) RotX( float64 ) RotY( float64 ) RotZ( float64 ) Scale( float64 float64 float64 ) Sub( Shape ) Transl( float64 float64 float64 ) Xor( Shape )`
- `Line2D(float64, float64, float64, float64, float64, string) Shape`
  - methods: `Add( Shape ) Intersect( Shape ) Inverse( ) Repeat( float64 float64 float64 ) RotX( float64 ) RotY( float64 ) RotZ( float64 ) Scale( float64 float64 float64 ) Sub( Shape ) Transl( float64 float64 float64 ) Xor( Shape )`
- `Rect(float64, float64) Shape`
  - methods: `Add( Shape ) Intersect( Shape ) Inverse( ) Repeat( float64 float64 float64 ) RotX( float64 ) RotY( float64 ) RotZ( float64 ) Scale( float64 float64 float64 ) Sub( Shape ) Transl( float64 float64 float64 ) Xor( Shape )`
- `Square(float64) Shape`
  - methods: `Add( Shape ) Intersect( Shape ) Inverse( ) Repeat( float64 float64 float64 ) RotX( float64 ) RotY( float64 ) RotZ( float64 ) Scale( float64 float64 float64 ) Sub( Shape ) Transl( float64 float64 float64 ) Xor( Shape )`
- `Superball(float64, float64) Shape`
  - methods: `Add( Shape ) Intersect( Shape ) Inverse( ) Repeat( float64 float64 float64 ) RotX( float64 ) RotY( float64 ) RotZ( float64 ) Scale( float64 float64 float64 ) Sub( Shape ) Transl( float64 float64 float64 ) Xor( Shape )`
- `Triangle(float64, float64, float64, float64, float64, float64) Shape`
  - methods: `Add( Shape ) Intersect( Shape ) Inverse( ) Repeat( float64 float64 float64 ) RotX( float64 ) RotY( float64 ) RotZ( float64 ) Scale( float64 float64 float64 ) Sub( Shape ) Transl( float64 float64 float64 ) Xor( Shape )`
- `Universe() Shape`
  - methods: `Add( Shape ) Intersect( Shape ) Inverse( ) Repeat( float64 float64 float64 ) RotX( float64 ) RotY( float64 ) RotZ( float64 ) Scale( float64 float64 float64 ) Sub( Shape ) Transl( float64 float64 float64 ) Xor( Shape )`
- `VoxelShape(Slice, float64, float64, float64) Shape`
  - methods: `Add( Shape ) Intersect( Shape ) Inverse( ) Repeat( float64 float64 float64 ) RotX( float64 ) RotY( float64 ) RotZ( float64 ) Scale( float64 float64 float64 ) Sub( Shape ) Transl( float64 float64 float64 ) Xor( Shape )`
- `XRange(float64, float64) Shape`
  - methods: `Add( Shape ) Intersect( Shape ) Inverse( ) Repeat( float64 float64 float64 ) RotX( float64 ) RotY( float64 ) RotZ( float64 ) Scale( float64 float64 float64 ) Sub( Shape ) Transl( float64 float64 float64 ) Xor( Shape )`
- `YRange(float64, float64) Shape`
  - methods: `Add( Shape ) Intersect( Shape ) Inverse( ) Repeat( float64 float64 float64 ) RotX( float64 ) RotY( float64 ) RotZ( float64 ) Scale( float64 float64 float64 ) Sub( Shape ) Transl( float64 float64 float64 ) Xor( Shape )`
- `ZRange(float64, float64) Shape`
  - methods: `Add( Shape ) Intersect( Shape ) Inverse( ) Repeat( float64 float64 float64 ) RotX( float64 ) RotY( float64 ) RotZ( float64 ) Scale( float64 float64 float64 ) Sub( Shape ) Transl( float64 float64 float64 ) Xor( Shape )`

## Material regions

- `DefRegion(int, Shape)`
- `DefRegionCell(int, int, int, int)`
- `NREGION`
- `RedefRegion(int, int)`
- `regions`
  - methods: `Average( ) EvalTo( Slice ) GetCell( int int int ) Gpu( ) HostArray( ) HostList( ) LoadFile( string ) SetCell( int int int int )`

## Initial magnetization

- `m`
  - methods: `Average( ) Buffer( ) Comp( int ) EvalTo( Slice ) GetCell( int int int ) LoadFile( string ) Quantity( ) Region( int ) Set( Config ) SetArray( Slice ) SetCell( int int int data.Vector ) SetInShape( Shape Config ) SetRegion( int Config )`
- `Antivortex(int, int) Config`
  - methods: `Add( float64 Config ) RotZ( float64 ) Scale( float64 float64 float64 ) Transl( float64 float64 float64 )`
- `BlochSkyrmion(int, int) Config`
  - methods: `Add( float64 Config ) RotZ( float64 ) Scale( float64 float64 float64 ) Transl( float64 float64 float64 )`
- `Conical(data.Vector, data.Vector, float64) Config`
  - methods: `Add( float64 Config ) RotZ( float64 ) Scale( float64 float64 float64 ) Transl( float64 float64 float64 )`
- `CurrentMag() Config`
  - methods: `Add( float64 Config ) RotZ( float64 ) Scale( float64 float64 float64 ) Transl( float64 float64 float64 )`
- `Helical(data.Vector) Config`
  - methods: `Add( float64 Config ) RotZ( float64 ) Scale( float64 float64 float64 ) Transl( float64 float64 float64 )`
- `HopfionCompactSupport(float64, float64) Config`
  - methods: `Add( float64 Config ) RotZ( float64 ) Scale( float64 float64 float64 ) Transl( float64 float64 float64 )`
- `NeelSkyrmion(int, int) Config`
  - methods: `Add( float64 Config ) RotZ( float64 ) Scale( float64 float64 float64 ) Transl( float64 float64 float64 )`
- `RandomMag() Config`
  - methods: `Add( float64 Config ) RotZ( float64 ) Scale( float64 float64 float64 ) Transl( float64 float64 float64 )`
- `RandomMagSeed(int) Config`
  - methods: `Add( float64 Config ) RotZ( float64 ) Scale( float64 float64 float64 ) Transl( float64 float64 float64 )`
- `TwoDomain(float64, float64, float64, float64, float64, float64, float64, float64, float64) Config`
  - methods: `Add( float64 Config ) RotZ( float64 ) Scale( float64 float64 float64 ) Transl( float64 float64 float64 )`
- `Uniform(float64, float64, float64) Config`
  - methods: `Add( float64 Config ) RotZ( float64 ) Scale( float64 float64 float64 ) Transl( float64 float64 float64 )`
- `Vortex(int, int) Config`
  - methods: `Add( float64 Config ) RotZ( float64 ) Scale( float64 float64 float64 ) Transl( float64 float64 float64 )`
- `VortexWall(float64, float64, int, int) Config`
  - methods: `Add( float64 Config ) RotZ( float64 ) Scale( float64 float64 float64 ) Transl( float64 float64 float64 )`

## Material parameters

- `Aex`
  - methods: `Average( ) EvalTo( Slice ) GetRegion( int ) IsUniform( ) MSlice( ) Region( int ) Set( float64 ) SetRegion( int ScalarFunction ) SetRegionFuncGo( int func() float64 ) SetRegionValueGo( int float64 )`
- `alpha`
  - methods: `Average( ) EvalTo( Slice ) GetRegion( int ) IsUniform( ) MSlice( ) Region( int ) Set( float64 ) SetRegion( int ScalarFunction ) SetRegionFuncGo( int func() float64 ) SetRegionValueGo( int float64 )`
- `anisC1`
  - methods: `Average( ) Comp( int ) EvalTo( Slice ) GetRegion( int ) IsUniform( ) MSlice( ) Region( int ) SetRegion( int VectorFunction ) SetRegionFn( int func() [3]float64 )`
- `anisC2`
  - methods: `Average( ) Comp( int ) EvalTo( Slice ) GetRegion( int ) IsUniform( ) MSlice( ) Region( int ) SetRegion( int VectorFunction ) SetRegionFn( int func() [3]float64 )`
- `anisU`
  - methods: `Average( ) Comp( int ) EvalTo( Slice ) GetRegion( int ) IsUniform( ) MSlice( ) Region( int ) SetRegion( int VectorFunction ) SetRegionFn( int func() [3]float64 )`
- `B1`
  - methods: `Average( ) EvalTo( Slice ) GetRegion( int ) IsUniform( ) MSlice( ) Region( int ) Set( float64 ) SetRegion( int ScalarFunction ) SetRegionFuncGo( int func() float64 ) SetRegionValueGo( int float64 )`
- `B2`
  - methods: `Average( ) EvalTo( Slice ) GetRegion( int ) IsUniform( ) MSlice( ) Region( int ) Set( float64 ) SetRegion( int ScalarFunction ) SetRegionFuncGo( int func() float64 ) SetRegionValueGo( int float64 )`
- `Dbulk`
  - methods: `Average( ) EvalTo( Slice ) GetRegion( int ) IsUniform( ) MSlice( ) Region( int ) Set( float64 ) SetRegion( int ScalarFunction ) SetRegionFuncGo( int func() float64 ) SetRegionValueGo( int float64 )`
- `Dind`
  - methods: `Average( ) EvalTo( Slice ) GetRegion( int ) IsUniform( ) MSlice( ) Region( int ) Set( float64 ) SetRegion( int ScalarFunction ) SetRegionFuncGo( int func() float64 ) SetRegionValueGo( int float64 )`
- `EpsilonPrime`
  - methods: `Average( ) EvalTo( Slice ) GetRegion( int ) IsUniform( ) MSlice( ) Region( int ) Set( float64 ) SetRegion( int ScalarFunction ) SetRegionFuncGo( int func() float64 ) SetRegionValueGo( int float64 )`
- `FreeLayerThickness`
  - methods: `Average( ) EvalTo( Slice ) GetRegion( int ) IsUniform( ) MSlice( ) Region( int ) Set( float64 ) SetRegion( int ScalarFunction ) SetRegionFuncGo( int func() float64 ) SetRegionValueGo( int float64 )`
- `frozenspins`
  - methods: `Average( ) EvalTo( Slice ) GetRegion( int ) IsUniform( ) MSlice( ) Region( int ) Set( float64 ) SetRegion( int ScalarFunction ) SetRegionFuncGo( int func() float64 ) SetRegionValueGo( int float64 )`
- `Kc1`
  - methods: `Average( ) EvalTo( Slice ) GetRegion( int ) IsUniform( ) MSlice( ) Region( int ) Set( float64 ) SetRegion( int ScalarFunction ) SetRegionFuncGo( int func() float64 ) SetRegionValueGo( int float64 )`
- `Kc2`
  - methods: `Average( ) EvalTo( Slice ) GetRegion( int ) IsUniform( ) MSlice( ) Region( int ) Set( float64 ) SetRegion( int ScalarFunction ) SetRegionFuncGo( int func() float64 ) SetRegionValueGo( int float64 )`
- `Kc3`
  - methods: `Average( ) EvalTo( Slice ) GetRegion( int ) IsUniform( ) MSlice( ) Region( int ) Set( float64 ) SetRegion( int ScalarFunction ) SetRegionFuncGo( int func() float64 ) SetRegionValueGo( int float64 )`
- `Ku1`
  - methods: `Average( ) EvalTo( Slice ) GetRegion( int ) IsUniform( ) MSlice( ) Region( int ) Set( float64 ) SetRegion( int ScalarFunction ) SetRegionFuncGo( int func() float64 ) SetRegionValueGo( int float64 )`
- `Ku2`
  - methods: `Average( ) EvalTo( Slice ) GetRegion( int ) IsUniform( ) MSlice( ) Region( int ) Set( float64 ) SetRegion( int ScalarFunction ) SetRegionFuncGo( int func() float64 ) SetRegionValueGo( int float64 )`
- `Lambda`
  - methods: `Average( ) EvalTo( Slice ) GetRegion( int ) IsUniform( ) MSlice( ) Region( int ) Set( float64 ) SetRegion( int ScalarFunction ) SetRegionFuncGo( int func() float64 ) SetRegionValueGo( int float64 )`
- `Msat`
  - methods: `Average( ) EvalTo( Slice ) GetRegion( int ) IsUniform( ) MSlice( ) Region( int ) Set( float64 ) SetRegion( int ScalarFunction ) SetRegionFuncGo( int func() float64 ) SetRegionValueGo( int float64 )`
- `NoDemagSpins`
  - methods: `Average( ) EvalTo( Slice ) GetRegion( int ) IsUniform( ) MSlice( ) Region( int ) Set( float64 ) SetRegion( int ScalarFunction ) SetRegionFuncGo( int func() float64 ) SetRegionValueGo( int float64 )`
- `Pol`
  - methods: `Average( ) EvalTo( Slice ) GetRegion( int ) IsUniform( ) MSlice( ) Region( int ) Set( float64 ) SetRegion( int ScalarFunction ) SetRegionFuncGo( int func() float64 ) SetRegionValueGo( int float64 )`
- `Temp`
  - methods: `Average( ) EvalTo( Slice ) GetRegion( int ) IsUniform( ) MSlice( ) Region( int ) Set( float64 ) SetRegion( int ScalarFunction ) SetRegionFuncGo( int func() float64 ) SetRegionValueGo( int float64 )`
- `xi`
  - methods: `Average( ) EvalTo( Slice ) GetRegion( int ) IsUniform( ) MSlice( ) Region( int ) Set( float64 ) SetRegion( int ScalarFunction ) SetRegionFuncGo( int func() float64 ) SetRegionValueGo( int float64 )`

## Excitation

- `B_ext`
  - methods: `Add( Slice ScalarFunction ) AddGo( Slice func() float64 ) AddTo( Slice ) Average( ) Comp( int ) EvalTo( Slice ) IsUniform( ) MSlice( ) Region( int ) RemoveExtraTerms( ) Set( data.Vector ) SetRegion( int VectorFunction ) SetRegionFn( int func() [3]float64 )`
- `FixedLayer`
  - methods: `Add( Slice ScalarFunction ) AddGo( Slice func() float64 ) AddTo( Slice ) Average( ) Comp( int ) EvalTo( Slice ) IsUniform( ) MSlice( ) Region( int ) RemoveExtraTerms( ) Set( data.Vector ) SetRegion( int VectorFunction ) SetRegionFn( int func() [3]float64 )`
- `J`
  - methods: `Add( Slice ScalarFunction ) AddGo( Slice func() float64 ) AddTo( Slice ) Average( ) Comp( int ) EvalTo( Slice ) IsUniform( ) MSlice( ) Region( int ) RemoveExtraTerms( ) Set( data.Vector ) SetRegion( int VectorFunction ) SetRegionFn( int func() [3]float64 )`
- `FunctionFromDatafile(string, int, int, string) func(float64) float64`

## Spin currents

- `DisableSlonczewskiTorque`
- `DisableZhangLiTorque`
- `EpsilonPrime`
  - methods: `Average( ) EvalTo( Slice ) GetRegion( int ) IsUniform( ) MSlice( ) Region( int ) Set( float64 ) SetRegion( int ScalarFunction ) SetRegionFuncGo( int func() float64 ) SetRegionValueGo( int float64 )`
- `FixedLayer`
  - methods: `Add( Slice ScalarFunction ) AddGo( Slice func() float64 ) AddTo( Slice ) Average( ) Comp( int ) EvalTo( Slice ) IsUniform( ) MSlice( ) Region( int ) RemoveExtraTerms( ) Set( data.Vector ) SetRegion( int VectorFunction ) SetRegionFn( int func() [3]float64 )`
- `FIXEDLAYER_BOTTOM`
- `FIXEDLAYER_TOP`
- `FixedLayerPosition`
- `FreeLayerThickness`
  - methods: `Average( ) EvalTo( Slice ) GetRegion( int ) IsUniform( ) MSlice( ) Region( int ) Set( float64 ) SetRegion( int ScalarFunction ) SetRegionFuncGo( int func() float64 ) SetRegionValueGo( int float64 )`
- `J`
  - methods: `Add( Slice ScalarFunction ) AddGo( Slice func() float64 ) AddTo( Slice ) Average( ) Comp( int ) EvalTo( Slice ) IsUniform( ) MSlice( ) Region( int ) RemoveExtraTerms( ) Set( data.Vector ) SetRegion( int VectorFunction ) SetRegionFn( int func() [3]float64 )`
- `Lambda`
  - methods: `Average( ) EvalTo( Slice ) GetRegion( int ) IsUniform( ) MSlice( ) Region( int ) Set( float64 ) SetRegion( int ScalarFunction ) SetRegionFuncGo( int func() float64 ) SetRegionValueGo( int float64 )`
- `Pol`
  - methods: `Average( ) EvalTo( Slice ) GetRegion( int ) IsUniform( ) MSlice( ) Region( int ) Set( float64 ) SetRegion( int ScalarFunction ) SetRegionFuncGo( int func() float64 ) SetRegionValueGo( int float64 )`
- `xi`
  - methods: `Average( ) EvalTo( Slice ) GetRegion( int ) IsUniform( ) MSlice( ) Region( int ) Set( float64 ) SetRegion( int ScalarFunction ) SetRegionFuncGo( int func() float64 ) SetRegionValueGo( int float64 )`

## Magnetic Force Microscopy

- `MFM`
  - methods: `Average( ) EvalTo( Slice ) Region( int )`
- `MFMDipole`
- `MFMLift`

## Output quantities

- `B_anis`
  - methods: `Average( ) Comp( int ) EvalTo( Slice ) HostCopy( ) Region( int )`
- `B_custom`
  - methods: `Average( ) Comp( int ) EvalTo( Slice ) HostCopy( ) Region( int )`
- `B_demag`
  - methods: `Average( ) Comp( int ) EvalTo( Slice ) HostCopy( ) Region( int )`
- `B_eff`
  - methods: `Average( ) Comp( int ) EvalTo( Slice ) HostCopy( ) Region( int )`
- `B_exch`
  - methods: `Average( ) Comp( int ) EvalTo( Slice ) HostCopy( ) Region( int )`
- `B_mel`
  - methods: `Average( ) Comp( int ) EvalTo( Slice ) HostCopy( ) Region( int )`
- `B_therm`
  - methods: `AddTo( Slice ) EvalTo( Slice )`
- `DindCoupling`
  - methods: `Average( ) EvalTo( Slice ) Region( int )`
- `dt`
  - methods: `Average( ) EvalTo( Slice ) Get( )`
- `E_anis`
  - methods: `Average( ) EvalTo( Slice ) Get( )`
- `E_custom`
  - methods: `Average( ) EvalTo( Slice ) Get( )`
- `E_demag`
  - methods: `Average( ) EvalTo( Slice ) Get( )`
- `E_exch`
  - methods: `Average( ) EvalTo( Slice ) Get( )`
- `E_mel`
  - methods: `Average( ) EvalTo( Slice ) Get( )`
- `E_therm`
  - methods: `Average( ) EvalTo( Slice ) Get( )`
- `E_total`
  - methods: `Average( ) EvalTo( Slice ) Get( )`
- `E_Zeeman`
  - methods: `Average( ) EvalTo( Slice ) Get( )`
- `Edens_anis`
  - methods: `Average( ) EvalTo( Slice ) Region( int )`
- `Edens_custom`
  - methods: `Average( ) EvalTo( Slice ) Region( int )`
- `Edens_demag`
  - methods: `Average( ) EvalTo( Slice ) Region( int )`
- `Edens_exch`
  - methods: `Average( ) EvalTo( Slice ) Region( int )`
- `Edens_mel`
  - methods: `Average( ) EvalTo( Slice ) Region( int )`
- `Edens_therm`
  - methods: `Average( ) EvalTo( Slice ) Region( int )`
- `Edens_total`
  - methods: `Average( ) EvalTo( Slice ) Region( int )`
- `Edens_Zeeman`
  - methods: `Average( ) EvalTo( Slice ) Region( int )`
- `ExchCoupling`
  - methods: `Average( ) EvalTo( Slice ) Region( int )`
- `F_mel`
  - methods: `Average( ) Comp( int ) EvalTo( Slice ) HostCopy( ) Region( int )`
- `geom`
  - methods: `Average( ) EvalTo( Slice ) GetCell( int int int ) Gpu( )`
- `LastErr`
  - methods: `Average( ) EvalTo( Slice ) Get( )`
- `LLtorque`
  - methods: `Average( ) Comp( int ) EvalTo( Slice ) HostCopy( ) Region( int )`
- `m`
  - methods: `Average( ) Buffer( ) Comp( int ) EvalTo( Slice ) GetCell( int int int ) LoadFile( string ) Quantity( ) Region( int ) Set( Config ) SetArray( Slice ) SetCell( int int int data.Vector ) SetInShape( Shape Config ) SetRegion( int Config )`
- `m_full`
  - methods: `Average( ) Comp( int ) EvalTo( Slice ) HostCopy( ) Region( int )`
- `MaxAngle`
  - methods: `Average( ) EvalTo( Slice ) Get( )`
- `maxTorque`
  - methods: `Average( ) EvalTo( Slice ) Get( )`
- `MFM`
  - methods: `Average( ) EvalTo( Slice ) Region( int )`
- `NEval`
  - methods: `Average( ) EvalTo( Slice ) Get( )`
- `PeakErr`
  - methods: `Average( ) EvalTo( Slice ) Get( )`
- `spinAngle`
  - methods: `Average( ) EvalTo( Slice ) Region( int )`
- `STTorque`
  - methods: `Average( ) Comp( int ) EvalTo( Slice ) HostCopy( ) Region( int )`
- `torque`
  - methods: `Average( ) Comp( int ) EvalTo( Slice ) HostCopy( ) Region( int )`

## Slicing and dicing output

- `Crop(Quantity, int, int, int, int, int, int) *cropped`
  - methods: `Average( ) EvalTo( Slice )`
- `CropLayer(Quantity, int) *cropped`
  - methods: `Average( ) EvalTo( Slice )`
- `CropRegion(Quantity, int) *cropped`
  - methods: `Average( ) EvalTo( Slice )`
- `CropX(Quantity, int, int) *cropped`
  - methods: `Average( ) EvalTo( Slice )`
- `CropY(Quantity, int, int) *cropped`
  - methods: `Average( ) EvalTo( Slice )`
- `CropZ(Quantity, int, int) *cropped`
  - methods: `Average( ) EvalTo( Slice )`

## Scheduling output

- `AutoSave(Quantity, float64)`
- `AutoSnapshot(Quantity, float64)`
- `DUMP`
- `FilenameFormat`
- `Flush()`
- `Fprintln(string, ...interface {})`
- `OutputFormat`
- `OVF1_BINARY`
- `OVF1_TEXT`
- `OVF2_BINARY`
- `OVF2_TEXT`
- `Print(...interface {})`
- `Save(Quantity)`
- `SaveAs(Quantity, string)`
- `Snapshot(Quantity)`
- `SnapshotAs(Quantity, string)`
- `SnapshotFormat`
- `sprint(...interface {}) string`
- `sprintf(string, ...interface {}) string`
- `TableAdd(Quantity)`
- `TableAddVar(ScalarFunction, string, string)`
- `TableAutoSave(float64)`
- `TablePrint(...interface {})`
- `TableSave()`

## Running

- `Minimize() bool`
- `Relax() bool`
- `Run(float64)`
- `RunWhile(func() bool)`
- `Steps(int)`
- `dt`
  - methods: `Average( ) EvalTo( Slice ) Get( )`
- `FixDt`
- `Headroom`
- `LastErr`
  - methods: `Average( ) EvalTo( Slice ) Get( )`
- `MaxDt`
- `MaxErr`
- `MinDt`
- `MinimizerSamples`
- `MinimizerStop`
- `MinimizeWallClockTime`
- `NEval`
  - methods: `Average( ) EvalTo( Slice ) Get( )`
- `PeakErr`
  - methods: `Average( ) EvalTo( Slice ) Get( )`
- `RelaxTorqueThreshold`
- `RelaxWallClockTime`
- `step`
- `t`
- `SetSolver(int)`

## Moving simulation window

- `Shift(int)`
- `TotalShift`
- `ext_centerBubble()`
- `ext_centerWall(int)`
- `ext_centerWallInLayer(int, int)`
- `ext_centerWallInRegion(int, int)`
- `ext_rmSurfaceCharge(int, float64, float64)`
- `EdgeCarryShift`
- `ShiftGeom`
- `ShiftM`
- `ShiftMagD`
  - methods: `Add( data.Vector ) Cross( data.Vector ) Div( float64 ) Dot( data.Vector ) Len( ) MAdd( float64 data.Vector ) Mul( float64 ) Sub( data.Vector ) X( ) Y( ) Z( )`
- `ShiftMagL`
  - methods: `Add( data.Vector ) Cross( data.Vector ) Div( float64 ) Dot( data.Vector ) Len( ) MAdd( float64 data.Vector ) Mul( float64 ) Sub( data.Vector ) X( ) Y( ) Z( )`
- `ShiftMagR`
  - methods: `Add( data.Vector ) Cross( data.Vector ) Div( float64 ) Dot( data.Vector ) Len( ) MAdd( float64 data.Vector ) Mul( float64 ) Sub( data.Vector ) X( ) Y( ) Z( )`
- `ShiftMagU`
  - methods: `Add( data.Vector ) Cross( data.Vector ) Div( float64 ) Dot( data.Vector ) Len( ) MAdd( float64 data.Vector ) Mul( float64 ) Sub( data.Vector ) X( ) Y( ) Z( )`
- `ShiftRegions`

## Extensions

- `ext_AllRegionShapes() func(int) Shape`
- `ext_BackGroundTilt`
- `ext_bubbledist`
  - methods: `Average( ) EvalTo( Slice ) Get( )`
- `ext_BubbleMz`
- `ext_bubblepos`
  - methods: `Average( ) EvalTo( Slice ) Get( )`
- `ext_bubblespeed`
  - methods: `Average( ) EvalTo( Slice ) Get( )`
- `ext_centerBubble()`
- `ext_centerWall(int)`
- `ext_centerWallInLayer(int, int)`
- `ext_centerWallInRegion(int, int)`
- `ext_corepos`
  - methods: `Average( ) EvalTo( Slice ) Get( )`
- `ext_dwpos`
  - methods: `Average( ) EvalTo( Slice ) Get( )`
- `ext_dwspeed`
  - methods: `Average( ) EvalTo( Slice ) Get( )`
- `ext_dwtilt`
  - methods: `Average( ) EvalTo( Slice ) Get( )`
- `ext_dwxpos`
  - methods: `Average( ) EvalTo( Slice ) Get( )`
- `ext_emergentmagneticfield_fivepointstencil`
  - methods: `Average( ) Comp( int ) EvalTo( Slice ) HostCopy( ) Region( int )`
- `ext_emergentmagneticfield_solidangle`
  - methods: `Average( ) Comp( int ) EvalTo( Slice ) HostCopy( ) Region( int )`
- `ext_emergentmagneticfield_twopointstencil`
  - methods: `Average( ) Comp( int ) EvalTo( Slice ) HostCopy( ) Region( int )`
- `ext_enableCenterBubbleX`
- `ext_enableCenterBubbleY`
- `ext_EnableUnsafe()`
- `ext_GeomEdge(string) Shape`
  - methods: `Add( Shape ) Intersect( Shape ) Inverse( ) Repeat( float64 float64 float64 ) RotX( float64 ) RotY( float64 ) RotZ( float64 ) Scale( float64 float64 float64 ) Sub( Shape ) Transl( float64 float64 float64 ) Xor( Shape )`
- `ext_grainboundaries(int, int, int, float64, int)`
- `ext_grainboundary_edgeX`
- `ext_grainboundary_edgeY`
- `ext_grainboundary_edgeZ`
- `ext_grainCutShape`
- `ext_hopfindex_fivepointstencil`
  - methods: `Average( ) EvalTo( Slice ) Get( )`
- `ext_hopfindex_solidangle`
  - methods: `Average( ) EvalTo( Slice ) Get( )`
- `ext_hopfindex_solidanglefourier`
  - methods: `Average( ) EvalTo( Slice ) Get( )`
- `ext_hopfindex_twopointstencil`
  - methods: `Average( ) EvalTo( Slice ) Get( )`
- `ext_hopfindexdensity_fivepointstencil`
  - methods: `Average( ) EvalTo( Slice ) Region( int )`
- `ext_hopfindexdensity_solidangle`
  - methods: `Average( ) EvalTo( Slice ) Region( int )`
- `ext_hopfindexdensity_twopointstencil`
  - methods: `Average( ) EvalTo( Slice ) Region( int )`
- `ext_InitGeomFromOVF(string)`
- `ext_InterDind(int, int, float64)`
- `ext_InterExchange(int, int, float64)`
- `ext_make3dgrains(float64, int, int, Shape, int)`
- `ext_makegrains(float64, int, int)`
- `ext_phi`
  - methods: `Average( ) EvalTo( Slice ) Region( int )`
- `ext_rmSurfaceCharge(int, float64, float64)`
- `ext_ScaleDind(int, int, float64)`
- `ext_ScaleExchange(int, int, float64)`
- `ext_theta`
  - methods: `Average( ) EvalTo( Slice ) Region( int )`
- `ext_topologicalcharge`
  - methods: `Average( ) EvalTo( Slice ) Get( )`
- `ext_topologicalchargedensity`
  - methods: `Average( ) EvalTo( Slice ) Region( int )`
- `ext_topologicalchargedensitylattice`
  - methods: `Average( ) EvalTo( Slice ) Region( int )`
- `ext_topologicalchargelattice`
  - methods: `Average( ) EvalTo( Slice ) Get( )`

## Custom quantities

- `Add(Quantity, Quantity) Quantity`
  - methods: `EvalTo( )`
- `Const(float64) Quantity`
  - methods: `EvalTo( )`
- `ConstVector(float64, float64, float64) Quantity`
  - methods: `EvalTo( )`
- `Cross(Quantity, Quantity) Quantity`
  - methods: `EvalTo( )`
- `CustomQuantity(Slice) Quantity`
  - methods: `EvalTo( )`
- `Div(Quantity, Quantity) Quantity`
  - methods: `EvalTo( )`
- `Dot(Quantity, Quantity) Quantity`
  - methods: `EvalTo( )`
- `Madd(Quantity, Quantity, float64, float64) *mAddition`
  - methods: `EvalTo( Slice )`
- `Masked(Quantity, Shape) Quantity`
  - methods: `EvalTo( )`
- `Mul(Quantity, Quantity) Quantity`
  - methods: `EvalTo( )`
- `MulMV(Quantity, Quantity, Quantity, Quantity) Quantity`
  - methods: `EvalTo( )`
- `Normalized(Quantity) Quantity`
  - methods: `EvalTo( )`
- `RunningAverage(Quantity) Quantity`
  - methods: `EvalTo( )`
- `Shifted(Quantity, int, int, int) Quantity`
  - methods: `EvalTo( )`
- `Sum(Quantity) float64`
- `SumVector(Quantity) data.Vector`
  - methods: `Add( data.Vector ) Cross( data.Vector ) Div( float64 ) Dot( data.Vector ) Len( ) MAdd( float64 data.Vector ) Mul( float64 ) Sub( data.Vector ) X( ) Y( ) Z( )`

## Custom effective field terms

- `AddEdensTerm(Quantity)`
- `AddFieldTerm(Quantity)`
- `B_custom`
  - methods: `Average( ) Comp( int ) EvalTo( Slice ) HostCopy( ) Region( int )`
- `E_custom`
  - methods: `Average( ) EvalTo( Slice ) Get( )`
- `Edens_custom`
  - methods: `Average( ) EvalTo( Slice ) Region( int )`
- `RemoveCustomEnergies()`
- `RemoveCustomFields()`

## Math

- `abs(float64) float64`
- `acos(float64) float64`
- `acosh(float64) float64`
- `asin(float64) float64`
- `asinh(float64) float64`
- `atan(float64) float64`
- `atan2(float64, float64) float64`
- `atanh(float64) float64`
- `cbrt(float64) float64`
- `ceil(float64) float64`
- `cos(float64) float64`
- `cosh(float64) float64`
- `erf(float64) float64`
- `erfc(float64) float64`
- `exp(float64) float64`
- `exp2(float64) float64`
- `expm1(float64) float64`
- `floor(float64) float64`
- `gamma(float64) float64`
- `heaviside(float64) float64`
- `hypot(float64, float64) float64`
- `ilogb(float64) int`
- `isInf(float64, int) bool`
- `isNaN(float64) bool`
- `j0(float64) float64`
- `j1(float64) float64`
- `jn(int, float64) float64`
- `ldexp(float64, int) float64`
- `log(float64) float64`
- `log10(float64) float64`
- `log1p(float64) float64`
- `log2(float64) float64`
- `logb(float64) float64`
- `max(float64, float64) float64`
- `min(float64, float64) float64`
- `Minimize() bool`
- `mod(float64, float64) float64`
- `norm(float64) float64`
- `pow(float64, float64) float64`
- `pow10(int) float64`
- `rand() float64`
- `randExp() float64`
- `randInt(int) int`
- `randNorm() float64`
- `Relax() bool`
- `remainder(float64, float64) float64`
- `Sign(float64) float64`
- `sin(float64) float64`
- `sinc(float64) float64`
- `sinh(float64) float64`
- `sqrt(float64) float64`
- `Sum(Quantity) float64`
- `tan(float64) float64`
- `tanh(float64) float64`
- `trunc(float64) float64`
- `y0(float64) float64`
- `y1(float64) float64`
- `yn(int, float64) float64`
- `inf`
- `pi`
- `false`
- `true`

## Misc

- `CellIndices() Slice`
  - methods: `CPUAccess( ) Comp( int ) DevPtr( int ) Disable( ) Free( ) GPUAccess( ) Get( int int int int ) Host( ) HostCopy( ) Index( int int int ) IsNil( ) Len( ) MemType( ) Scalars( ) Set( int int int int float64 ) SetScalar( int int int float64 ) SetVector( int int int data.Vector ) Size( ) Tensors( ) Vectors( )`
- `ClearPostSteps()`
- `DemagAccuracy`
- `DoPrecess`
- `EnableDemag`
- `Exit()`
- `Expect(string, float64, float64, float64)`
- `ExpectB(string, bool, bool)`
- `ExpectV(string, data.Vector, data.Vector, float64)`
- `exx`
  - methods: `Add( Slice ScalarFunction ) AddGo( Slice func() float64 ) AddTo( Slice ) Average( ) Comp( int ) EvalTo( Slice ) IsUniform( ) MSlice( ) Region( int ) RemoveExtraTerms( ) Set( float64 ) SetRegion( int ScalarFunction ) SetRegionFn( int func() [3]float64 )`
- `exy`
  - methods: `Add( Slice ScalarFunction ) AddGo( Slice func() float64 ) AddTo( Slice ) Average( ) Comp( int ) EvalTo( Slice ) IsUniform( ) MSlice( ) Region( int ) RemoveExtraTerms( ) Set( float64 ) SetRegion( int ScalarFunction ) SetRegionFn( int func() [3]float64 )`
- `exz`
  - methods: `Add( Slice ScalarFunction ) AddGo( Slice func() float64 ) AddTo( Slice ) Average( ) Comp( int ) EvalTo( Slice ) IsUniform( ) MSlice( ) Region( int ) RemoveExtraTerms( ) Set( float64 ) SetRegion( int ScalarFunction ) SetRegionFn( int func() [3]float64 )`
- `eyy`
  - methods: `Add( Slice ScalarFunction ) AddGo( Slice func() float64 ) AddTo( Slice ) Average( ) Comp( int ) EvalTo( Slice ) IsUniform( ) MSlice( ) Region( int ) RemoveExtraTerms( ) Set( float64 ) SetRegion( int ScalarFunction ) SetRegionFn( int func() [3]float64 )`
- `eyz`
  - methods: `Add( Slice ScalarFunction ) AddGo( Slice func() float64 ) AddTo( Slice ) Average( ) Comp( int ) EvalTo( Slice ) IsUniform( ) MSlice( ) Region( int ) RemoveExtraTerms( ) Set( float64 ) SetRegion( int ScalarFunction ) SetRegionFn( int func() [3]float64 )`
- `ezz`
  - methods: `Add( Slice ScalarFunction ) AddGo( Slice func() float64 ) AddTo( Slice ) Average( ) Comp( int ) EvalTo( Slice ) IsUniform( ) MSlice( ) Region( int ) RemoveExtraTerms( ) Set( float64 ) SetRegion( int ScalarFunction ) SetRegionFn( int func() [3]float64 )`
- `GammaLL`
- `Index2Coord(int, int, int) data.Vector`
  - methods: `Add( data.Vector ) Cross( data.Vector ) Div( float64 ) Dot( data.Vector ) Len( ) MAdd( float64 data.Vector ) Mul( float64 ) Sub( data.Vector ) X( ) Y( ) Z( )`
- `LoadFile(string) Slice`
  - methods: `CPUAccess( ) Comp( int ) DevPtr( int ) Disable( ) Free( ) GPUAccess( ) Get( int int int int ) Host( ) HostCopy( ) Index( int int int ) IsNil( ) Len( ) MemType( ) Scalars( ) Set( int int int int float64 ) SetScalar( int int int float64 ) SetVector( int int int data.Vector ) Size( ) Tensors( ) Vectors( )`
- `Mu0`
- `NewScalarMask(int, int, int) Slice`
  - methods: `CPUAccess( ) Comp( int ) DevPtr( int ) Disable( ) Free( ) GPUAccess( ) Get( int int int int ) Host( ) HostCopy( ) Index( int int int ) IsNil( ) Len( ) MemType( ) Scalars( ) Set( int int int int float64 ) SetScalar( int int int float64 ) SetVector( int int int data.Vector ) Size( ) Tensors( ) Vectors( )`
- `NewSlice(int, int, int, int) Slice`
  - methods: `CPUAccess( ) Comp( int ) DevPtr( int ) Disable( ) Free( ) GPUAccess( ) Get( int int int int ) Host( ) HostCopy( ) Index( int int int ) IsNil( ) Len( ) MemType( ) Scalars( ) Set( int int int int float64 ) SetScalar( int int int float64 ) SetVector( int int int data.Vector ) Size( ) Tensors( ) Vectors( )`
- `NewVectorMask(int, int, int) Slice`
  - methods: `CPUAccess( ) Comp( int ) DevPtr( int ) Disable( ) Free( ) GPUAccess( ) Get( int int int int ) Host( ) HostCopy( ) Index( int int int ) IsNil( ) Len( ) MemType( ) Scalars( ) Set( int int int int float64 ) SetScalar( int int int float64 ) SetVector( int int int data.Vector ) Size( ) Tensors( ) Vectors( )`
- `now() time.Time`
  - methods: `Add( time.Duration ) AddDate( int int int ) After( time.Time ) AppendBinary( []uint8 ) AppendFormat( []uint8 string ) AppendText( []uint8 ) Before( time.Time ) Clock( ) Compare( time.Time ) Date( ) Day( ) Equal( time.Time ) Format( string ) GoString( ) GobEncode( ) Hour( ) ISOWeek( ) In( *time.Location ) IsDST( ) IsZero( ) Local( ) Location( ) MarshalBinary( ) MarshalJSON( ) MarshalText( ) Minute( ) Month( ) Nanosecond( ) Round( time.Duration ) Second( ) Sub( time.Time ) Truncate( time.Duration ) UTC( ) Unix( ) UnixMicro( ) UnixMilli( ) UnixNano( ) Weekday( ) Year( ) YearDay( ) Zone( ) ZoneBounds( )`
- `OpenBC`
- `randSeed(int)`
- `since(time.Time) time.Duration`
  - methods: `Abs( ) Hours( ) Microseconds( ) Milliseconds( ) Minutes( ) Nanoseconds( ) Round( time.Duration ) Seconds( ) Truncate( time.Duration )`
- `ThermSeed(int)`
- `Vector(float64, float64, float64) data.Vector`
  - methods: `Add( data.Vector ) Cross( data.Vector ) Div( float64 ) Dot( data.Vector ) Len( ) MAdd( float64 data.Vector ) Mul( float64 ) Sub( data.Vector ) X( ) Y( ) Z( )`

## Source Notes

- Generated entries: 357.
- The official API page also includes narrative guidance for syntax, mesh sizing, implicit functions, output, running, and advanced features; keep those explanations in focused references such as `language_subset.md`, `api_patterns.md`, and `compatibility_notes.md`.

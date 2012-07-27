from pyplasm import *

import sys,time

start=time.clock()

# if you want to see intermediate results
debug_tower = True


ScaleFactor = 3.16655256
InternalBasementRadius = ScaleFactor*0.7
ExternalBasementRadius = ScaleFactor*3.2
BasementHeight = ScaleFactor*1.3
InternalFirstFloorRadius = ScaleFactor*1.2
ExternalFirstFloorRadius = ScaleFactor*2.5
WidthBasement = ExternalFirstFloorRadius - InternalFirstFloorRadius

InternalWallRadius = ScaleFactor*1.25
ExternalWallRadius = ScaleFactor*2.1
FirstFloorHeight = 3.15 * ScaleFactor
WallHeight = 9.35 * ScaleFactor
FirstRingPerimeter = 5.15 * ScaleFactor * PI
FirstRingColumnArcWidth = FirstRingPerimeter/12.0


# =======================================
# basament 1
# =======================================

def BuildBasement1(N_ext=64, N_int = 24):
    cyl_ext = CYLINDER(ExternalBasementRadius, BasementHeight/2.0, N_ext)
    cyl_int = CYLINDER(InternalBasementRadius, BasementHeight/2.0, N_int)
    return DIFF(cyl_ext, cyl_int)

Basement1 = BuildBasement1()

#if debug_tower:
#    VIEW(Basement1)

# =======================================
# Basement 2
# =======================================

def BuildBasement2(N = 64):
    tg_alpha = (ExternalBasementRadius - ExternalFirstFloorRadius) / (BasementHeight/2.0)
    hcone = tg_alpha * ExternalBasementRadius
    cone1 = CONE(ExternalBasementRadius, hcone, N)
    thebasament = INTERSECTION(Basement1, cone1)
    # Nice trick - mirroring the cone by scaling:
    reversed_cone = S(cone1, 1, 1, -1)
    tcone = tg_alpha * (ExternalBasementRadius - InternalBasementRadius)
    cone2 = T(reversed_cone, 0, 0, tcone)
    return DIFF(thebasament, cone2)

Basement2 = BuildBasement2()

#if debug_tower:
#    VIEW(Basement2)

# =======================================
# Basement
# =======================================

Basement = STRUCT(Basement1, T(Basement2, 0, 0, BasementHeight/2.0))

#if debug_tower:
#    VIEW(Basement)

# =======================================
# Basement
# =======================================

def BuildFirstFloor(N_ext = 64, N_int = 24):
        cyl_ext = CYLINDER(ExternalFirstFloorRadius, FirstFloorHeight, N_ext)
        cyl_int = CYLINDER(InternalFirstFloorRadius, FirstFloorHeight, N_int)
	return DIFF(cyl_ext, cyl_int)

FirstFloor = BuildFirstFloor()

#if debug_tower:
#    VIEW(FirstFloor)

# =======================================
# Basement
# =======================================

def BuildKernel(N_ext = 64, N_int = 24):
    cyl_ext = CYLINDER(ExternalWallRadius, WallHeight, N_ext)
    cyl_int = CYLINDER(InternalWallRadius, WallHeight, N_int)
    return DIFF(cyl_ext, cyl_int)

Kernel = BuildKernel()

#if debug_tower:
#    VIEW(Kernel)

# =======================================
# Terrace
# =======================================

def BuildTerrace(N = 64):
    tg_alpha = 0.05 * ExternalFirstFloorRadius / (0.095 * ScaleFactor)
    hcone = tg_alpha * 1.1 * ExternalFirstFloorRadius

    terrace1 = DIFF(
	CYLINDER(1.1*ExternalFirstFloorRadius,0.095*ScaleFactor/2, N),
	CYLINDER(ExternalWallRadius, 0.095*ScaleFactor/2, N)
    )

    cone1 = CONE(1.1 * ExternalFirstFloorRadius, hcone, N)
    wafer1 = INTERSECTION(terrace1, cone1)
    reverted_wafer1 = S(wafer1, 1, 1, -1)
    wafer1 = T(wafer1, 0, 0, 0.095*ScaleFactor/2)
    reverted_wafer1 = T(reverted_wafer1, 0, 0, 0.095*ScaleFactor/2)
    return STRUCT(reverted_wafer1, wafer1)

Terrace = BuildTerrace()

#if debug_tower:
#    VIEW(Terrace)

# =======================================
# Column_1
# =======================================

def Column_1 (angle, N = 24):
    unit = FirstRingColumnArcWidth/2.
    basis = CYLINDER(0.11 * ScaleFactor, 0.03 * ScaleFactor, N)
    fusto = CYLINDER(0.095 * ScaleFactor, 1.75*ScaleFactor, N)
    capitello = TRUNCONE(0.09 * ScaleFactor, 0.14 * ScaleFactor, 0.18 * ScaleFactor, N)
    box = BRICK(0.30 * ScaleFactor, 0.30 * ScaleFactor, 0.28 * ScaleFactor)
    box = T(box, -0.15 * ScaleFactor, -0.15 * ScaleFactor, 0)
    box1 = BRICK(0.30 * ScaleFactor, 0.30 * ScaleFactor, 0.05 * ScaleFactor)
    column = TOP(TOP(TOP(TOP(TOP(box, basis), fusto), basis), capitello),box1)
    column = T(column, 2.6 * ScaleFactor, 0, -0.2 * ScaleFactor)
    return R(column, 3, angle)

#if debug_tower:
#    VIEW(Column_1(PI/12))

# SIZE(object, i) returns the size of the object in the i-th axial direction:
ColumnScaling = (WallHeight / 6.0) / SIZE(Column_1(PI/24), 3)

# =======================================
# Column_2
# =======================================

def BuildBox1Column2():
    y = 0.13 * ScaleFactor
    x = -4*y
    z = y
    dy = math.tan(PI/36)*(-x)
    return MKPOL([[[0, y, 0], [0, -y, 0], [x, y-dy, 0], [x, dy-y, 0], [0, y, z], [0, -y, z], \
                   [x, y-dy, z], [x, dy-y, z]], [FROMTO([1,8])], [[1]]])

box1_column_2 = BuildBox1Column2()

def Column_2 (ANGLE, N=18):
    unit = FirstRingColumnArcWidth/2.0
    box0 = BRICK(0.24 * ScaleFactor, 0.24 * ScaleFactor, 0.06 * ScaleFactor)
    box0 = T(box0, -0.12*ScaleFactor, -0.12*ScaleFactor, 0)
    basis0 = CYLINDER(0.11 * ScaleFactor, ScaleFactor * 0.02, N)
    basis1 = CYLINDER(0.08 * ScaleFactor, 0.04 * ScaleFactor, N)
    basis2 = CYLINDER(0.09 * ScaleFactor, ScaleFactor * 0.02, N)
    fusto  = CYLINDER(0.07 * ScaleFactor, 1.40 * ScaleFactor, N)
    capitello = TRUNCONE(0.07 * ScaleFactor, 0.10 * ScaleFactor, 0.16 * ScaleFactor, N)
    A = TOP(TOP(TOP(TOP(TOP(TOP(box0, basis0), basis1), basis2), fusto), basis2), capitello)
    A = S(A, 1, 1, ColumnScaling)
    B = box1_column_2
    C = ALIGN(A, B, [1, MAX, MAX], [2, MID, MID], [3, MAX, MIN])

    ret = T(C, 2.53 * ScaleFactor, 0, 0.09 * ScaleFactor)
    return R(ret, 3, ANGLE)

#if debug_tower:
#    VIEW(Column_2(PI/12))

# =======================================
# Arch
# =======================================

def Arch (ARCH_arg_):
	R1 , R2 , W = ARCH_arg_
        cyl1 = CYLINDER(R2, W, 24)
        cyl2 = CYLINDER(R1, W, 24)
	return (COMP([
		COMP([
		COMP([
		OPTIMIZE, PLASM_R([1, 3])(PI/-2.0)]), PLASM_T(3)((W/-2.0))]), 
      PLASM_STRUCT]))([(RAISE(PLASM_NDIFF)([cyl1,(RAISE(SUM)([cyl2,(COMP([PLASM_T(2)((RAISE(PLASM_NDIFF)(R2))), CUBOID]))([R2, 2*R2, W])]))])), RAISE(PLASM_NDIFF)([(PLASM_T(2)((RAISE(PLASM_NDIFF)(R2))))((CUBOID([RAISE(PROD)([R2,SIN((PI/12))]), 2*R2, W]))),(PLASM_T(2)((RAISE(PLASM_NDIFF)(R1))))((CUBOID([RAISE(PROD)([R2,SIN((PI/12))]), RAISE(PROD)([2,R1]), W])))])])


def Build_ARC_1_1():
    unit = FirstRingColumnArcWidth/2.0

    a1 = Arch([0.8*unit, unit, unit/2.0])
    a2 = Arch([unit, 1.05*unit, unit/1.5])
    ret = STRUCT(a1, a2)

    return T(ret, 2.45 * ScaleFactor, 0, 2.30 * ScaleFactor)

Arc_1_1 = Build_ARC_1_1()

#if debug_tower:
#	VIEW(Arc_1_1)

# =======================================
# WALL_1_HOLE
# =======================================

def WALL_1_HOLE (WALL_1_HOLE_arg_):
	R2 , W = WALL_1_HOLE_arg_
	return (PLASM_T([1, 2])([2.45*ScaleFactor, 0]))(((COMP([COMP([PLASM_R([1, 3])(PI/-2.0), PLASM_S(3)(2)]), PLASM_T(3)((W/-2.0))]))((RAISE(PLASM_NDIFF)([CYLINDER(R2, 2.0*W, 24),(COMP([PLASM_T(2)((RAISE(PLASM_NDIFF)(R2))), CUBOID]))([R2, 2*R2, W])])))))


def BuildWall_1():
	UNIT = FirstRingColumnArcWidth/2.0
	THECYLINDER = RAISE(PLASM_NDIFF)([CYLINDER(RAISE(PROD)([1.08,ExternalFirstFloorRadius]), 1.1*UNIT, 24),CYLINDER(ExternalWallRadius, 1.1*UNIT, 24)])
	OTTUSANGLE = (RAISE(SUM)([(COMP([COMP([COMP([OPTIMIZE, PLASM_R([1, 2])((PI/12))]), PLASM_T(1)((-100))]), CUBOID]))([200, 100, 100]),(COMP([COMP([COMP([OPTIMIZE, PLASM_R([1, 2])((11*PI/12))]), PLASM_T(1)((-100))]), CUBOID]))([200, 100, 100])]))
	return PLASM_T(3)(2.30*ScaleFactor)(RAISE(PLASM_NDIFF)([RAISE(PLASM_NDIFF)([THECYLINDER, OTTUSANGLE]), WALL_1_HOLE([1.05*UNIT, UNIT/1.5])]))

Wall_1 = BuildWall_1()


if debug_tower:
    VIEW(Wall_1)



# =======================================
# FirstColumnRing
# =======================================

FirstColumnRing = (COMP([STRUCT, DOUBLE_DIESIS(12)]))([Column_1((PI/12)), Arc_1_1, Wall_1, R(3)((RAISE(DIV)([PI,6])))])


if debug_tower:
	lab.view(FirstColumnRing)


# =======================================
# Arc_2_1
# =======================================


def Arc_2_1 (ANGLE):
	UNIT = FirstRingColumnArcWidth/4
	ret_val = (COMP([COMP([OPTIMIZE, R(3)((ANGLE))]), T([1, 2, 3])([2.40*ScaleFactor, 0, 2.10*ScaleFactor*ColumnScaling])]))((STRUCT([(Arch([0.65*UNIT, 0.9*UNIT, RAISE(PROD)([1.5,UNIT])])),(Arch([0.9*UNIT, UNIT, UNIT/0.75]))])))
	return ret_val


# =======================================
# Wall_2
# =======================================

def Wall_2 (ANGLE):
	UNIT = FirstRingColumnArcWidth/4
	THECYLINDER = RAISE(DIFF)([CYLINDER([RAISE(PROD)([1.05,ExternalFirstFloorRadius]), RAISE(PROD)([1.35,UNIT])], 48),CYLINDER([ExternalWallRadius, RAISE(PROD)([1.35,UNIT])], 24)])
	ret_val = (COMP([COMP([OPTIMIZE, R(3)((ANGLE))]), T(3)((2.10*ScaleFactor*ColumnScaling))]))((RAISE(DIFF)([RAISE(DIFF)([THECYLINDER,Wall_2_Ottusangle]),Wall_2_Hole([UNIT, UNIT/0.75])])))
	return ret_val

Wall_2_Ottusangle = (RAISE(SUM)([(COMP([COMP([COMP([OPTIMIZE, R(3)((PI/24))]), T(1)((-100))]), CUBOID]))([200, 100, 100]),(COMP([COMP([COMP([OPTIMIZE, R(3)((23*PI/24))]), T(1)((-100))]), CUBOID]))([200, 100, 100])]))


if debug_tower:
	lab.view(Wall_2_Ottusangle)



# =======================================
# Wall_2_Hole
# =======================================

def Wall_2_Hole (WALL_2_HOLE_arg_):
	R2 , W = WALL_2_HOLE_arg_
	return (T([1, 2])([2.45*ScaleFactor, 0]))(((COMP([COMP([R(2)(PI/-2.0), S(3)(2)]), T(3)((W/-2.0))]))((RAISE(DIFF)([CYLINDER([R2, 2.0*W], 24),(COMP([T(2)((RAISE(DIFF)(R2))), CUBOID]))([R2, 2*R2, W])])))))


# =======================================
# SecondColumnRing
# =======================================

SecondColumnRing = (COMP([STRUCT, DOUBLE_DIESIS(24)]))([
		Column_2((PI/12)), 
		Arc_2_1((PI/24)), 
		Wall_2((PI/24)), 
		R(3)((PI/12))
      ])


if debug_tower:
	lab.view(SecondColumnRing)


RadiusSteps = 1.9*ScaleFactor
PitchSteps = ScaleFactor*7/1.5
AngleSteps = 21*PI/4
NumberOfSteps = 293
AlphaStep = RAISE(DIV)([RAISE(DIFF)(AngleSteps),NumberOfSteps])
ZetaStep = RAISE(DIV)([(RAISE(SUM)([FirstFloorHeight,WallHeight])),NumberOfSteps])
StepVolume = (COMP([T(1)((RAISE(DIFF)(RadiusSteps))), CUBOID]))((SCALARVECTPROD([[0.4, 0.11, 0.8],ScaleFactor])))



# =======================================
# Steps
# =======================================

def BuildStepsSegment ():
	TRANSLATIONS = DIESIS(17)((T(3)(ZetaStep)))
	ROTATIONS = DIESIS(17)((R(3)(AlphaStep)))
	OBJECTS = DIESIS(17)(StepVolume)
	return (COMP([COMP([COMP([OPTIMIZE, STRUCT]), CAT]), TRANS]))([TRANSLATIONS, ROTATIONS, OBJECTS])

StepSegment = BuildStepsSegment()

Steps = (COMP([COMP([OPTIMIZE, STRUCT]), DOUBLE_DIESIS(17)]))([
	StepSegment, 
	R(3)((RAISE(PROD)([17,AlphaStep]))), 
	T(3)((17*ZetaStep))
    ])


if debug_tower:
	lab(Steps)


# =======================================
# Fabric
# =======================================


Fabric = STRUCT([
		T(3)((RAISE(DIFF)(BasementHeight)))(Basement), 
		Steps, FirstFloor, 
		T(3)(FirstFloorHeight)(Kernel), 
		FirstColumnRing, 
		T(3)((RAISE(DIFF)([FirstFloorHeight,(0.095*ScaleFactor)]))), 
		Terrace, 
		(COMP([STRUCT, DOUBLE_DIESIS(5)]))([SecondColumnRing, T(3)((WallHeight/5)), Terrace])
		])

if debug_tower:
	lab.view(Fabric)


LASTFLOORHEIGHT = WallHeight/5


# =======================================
# TowerCap
# =======================================

def MySphere (RADIUS):
	def MYSPHERE0 (MYSPHERE0_arg_0):
		N , M = MYSPHERE0_arg_0
		FX = RAISE(PROD)([RAISE(PROD)([K(RADIUS),COMP([COMP([RAISE(DIFF), SIN]), S2])]),COMP([COS, S1])])
		FY = RAISE(PROD)([RAISE(PROD)([K(RADIUS),COMP([COS, S1])]),COMP([COS, S2])])
		FZ = RAISE(PROD)([K(RADIUS),COMP([SIN, S1])])
		domain = (RAISE(PROD)([INTERVALS(PI)(N),INTERVALS((2*PI))(M)]))
		ret_val = MAP(CONS([FX, FY, FZ]))(domain)
		return ret_val
	return MYSPHERE0

def buildTowerCap():
	LASTWALL = RAISE(DIFF)([CYLINDER([ExternalWallRadius, LASTFLOORHEIGHT], 24),CYLINDER([InternalWallRadius, LASTFLOORHEIGHT], 24)])
	return  STRUCT([
			LASTWALL,
			(RAISE(DIFF)([(COMP([COMP([T(3)(LASTFLOORHEIGHT), JOIN]), 
			PLASM_TRUNCONE([ExternalFirstFloorRadius, ExternalWallRadius, 
			RAISE(PROD)([0.4,ScaleFactor])])]))(24),
			JOIN((MySphere(ExternalWallRadius)([12, 24])))]))
	])


TowerCap = buildTowerCap()

if debug_tower:
	lab.view(TowerCap)


# =======================================
# Fabric
# =======================================

Fabric = \
	STRUCT([
		T(3)((RAISE(DIFF)(BasementHeight)))(Basement), 
		Steps, FirstFloor, 
		T(3)(FirstFloorHeight)(Kernel), 
		FirstColumnRing, 
		T(3)((RAISE(DIFF)([FirstFloorHeight,(0.095*ScaleFactor)]))), 
		Terrace, 
		(COMP([STRUCT, DOUBLE_DIESIS(6)]))([SecondColumnRing, T(3)(WallHeight/5), Terrace]), 
		T(3)((WallHeight)), 
		TowerCap
	])

if debug_tower:
	lab.view(Fabric)


Int7Height = 1.7*ScaleFactor
Ext7Height = 2.3*ScaleFactor
C11 = BEZIER(S1)([[InternalWallRadius, 0, 0], [InternalWallRadius, 0, Int7Height]])
C12 = BEZIER(S1)([[ExternalWallRadius, 0, 0], [ExternalWallRadius, 0, Ext7Height]])
SURF1 = BEZIER(S2)([C11, C12])
C21 = HERMITE([[InternalWallRadius, 0.0, Int7Height], [0.75, 0.0, (Ext7Height-0.25)], [-1.0, 0.0, 2.5], [-3.0, 0.0, 0.0]])
C22 = BEZIER(S1)([[ExternalWallRadius, 0.0, Ext7Height], [0.75, 0.0, Ext7Height]])
SURF2 = BEZIER(S2)([C21, C22])
C31 = BEZIER(S1)([[ExternalWallRadius, 0, Int7Height], [ExternalWallRadius, 0, Ext7Height]])
C32 = BEZIER(S1)([[(ExternalWallRadius+1), 0, Int7Height], [(ExternalWallRadius+1), 0, RAISE(DIV)([((Int7Height+Ext7Height)),2])]])
SURF3 = BEZIER(S2)([C31, C32])

# =======================================
# Solid
# =======================================


def Solid (SURF):
	return \
		[
			RAISE(DIFF)([
				(RAISE(PROD)([  COMP([S1,SURF])   ,COMP([COS, S3])])),
				(RAISE(PROD)([  COMP([S2,SURF])  ,COMP([SIN, S3])]))]), 
				 RAISE(SUM )([(RAISE(PROD)([    COMP([S2,SURF])  ,COMP([COS, S3])])),
				(RAISE(PROD)([   COMP([S1,SURF])    ,COMP([SIN, S3])]))
			]), 
			COMP([S3,SURF])
		]

# =======================================
# Out1
# =======================================


def buildOUT1():
	domain = (RAISE(PROD)([RAISE(PROD)([INTERVALS(1.0)(1),INTERVALS(1.0)(1)]),INTERVALS((3*PI/2))(18)]))
	return MAP((Solid(SURF1)))(domain)

Out1 = buildOUT1()

if debug_tower:
	lab.view(Out1)


# =======================================
# Out2
# =======================================


def buildOUT2():
	domain = (RAISE(PROD)([RAISE(PROD)([INTERVALS(1.0)(9),INTERVALS(1.0)(1)]),INTERVALS((3*PI/2))(18)]))
	return MAP((Solid(SURF1)))(domain)

Out2 = buildOUT2()


if debug_tower:
	lab.view(Out2)

# =======================================
# Out3
# =======================================


Out3 = MAP((Solid(SURF3)))((RAISE(PROD)([(COMP([SQR, INTERVALS(1.0)]))(1),INTERVALS((3*PI/2))(18)])))


if debug_tower:
	lab.view(Out3)


# =======================================
# Cap
# =======================================


Cap = STRUCT([Out1, Out2, Out3])

if debug_tower:
	lab.view(Cap)

# =======================================
# Column_B
# =======================================


def buildColumn_B():
	UNIT = FirstRingColumnArcWidth/2.0
	TRANSL = T([1, 2])([-0.12*ScaleFactor, -0.12*ScaleFactor])
	BOX0 = (COMP([TRANSL, CUBOID]))([0.24*ScaleFactor, 0.24*ScaleFactor, 0.06*ScaleFactor])
	BASIS0 = CYLINDER([0.11*ScaleFactor, ScaleFactor*0.02], 18)
	BASIS1 = CYLINDER([0.08*ScaleFactor, 0.04*ScaleFactor], 18)
	BASIS2 = CYLINDER([0.09*ScaleFactor, ScaleFactor*0.02], 18)
	FUSTO = CYLINDER([0.07*ScaleFactor, 1.40*ScaleFactor], 18)
	CAPITELLO = TRUNCONE([0.07*ScaleFactor, 0.10*ScaleFactor, 0.16*ScaleFactor], 18)
	BOX1 = BOX0
	return (COMP([OPTIMIZE, T([1, 2, 3])([-18.0*2.54*ScaleFactor/24.0, 0, 0.09*ScaleFactor])]))((ALIGN([[1, MAX, MAX], [2, MID, MID], [3, MAX, MIN]])([S(3)(ColumnScaling)((TOP([TOP([TOP([TOP([TOP([TOP([BOX0,BASIS0]),BASIS1]),BASIS2]),FUSTO]),BASIS2]),CAPITELLO]))),BOX1])))

Column_B = buildColumn_B()


if debug_tower:
	lab.view(Column_B)


# =======================================
# Arc_2_b
# =======================================




def buildARC_2_B():
	UNIT = FirstRingColumnArcWidth/4
	return (COMP([COMP([OPTIMIZE, R(3)((PI/18))]), T([1, 2, 3])([2.53*ScaleFactor*18.0/24.0, 0, ColumnScaling*2.08*ScaleFactor])]))((STRUCT([Arch([0.65*UNIT, 0.9*UNIT, 0.5*UNIT]),Arch([0.9*UNIT, 1.1*UNIT, 0.65*UNIT])])))

Arc_2_b = buildARC_2_B()

def buildARC_2_B():
	UNIT = FirstRingColumnArcWidth/4
	return (COMP([COMP([OPTIMIZE, R(3)((PI/18))]), T([1, 2, 3])([2.53*ScaleFactor*18.0/24.0, 0, ColumnScaling*2.08*ScaleFactor])]))((STRUCT([Arch([0.65*UNIT, 0.9*UNIT, 0.5*UNIT]),Arch([0.9*UNIT, 1.1*UNIT, 0.65*UNIT])])))

Arc_2_b = buildARC_2_B()



if debug_tower:
	VIEW(Arc_2_b)

# =======================================
# Wall_B_Ottusangle
# =======================================


def Wall_B (ANGLE):
	UNIT = FirstRingColumnArcWidth/4
	THECYLINDER = RAISE(DIFF)([CYLINDER([RAISE(PROD)([1.05,ExternalFirstFloorRadius]), RAISE(PROD)([1.35,UNIT])])(48),CYLINDER([ExternalWallRadius, RAISE(PROD)([1.35,UNIT])])(24)])
	ret_val = (COMP([COMP([OPTIMIZE, R(3)((ANGLE))]), T(3)((RAISE(PROD)([2.10*18.0*ScaleFactor/24.0,ColumnScaling])))]))((RAISE(DIFF)([RAISE(DIFF)([THECYLINDER,Wall_B_Ottusangle]),Wall_B_Hole([UNIT, UNIT/0.75])])))
	return ret_val


Wall_B_Ottusangle = (RAISE(SUM)([(COMP([COMP([COMP([OPTIMIZE, R(3)((PI/24))]), T(1)((-100))]), CUBOID]))([200, 100, 100]),(COMP([COMP([COMP([OPTIMIZE, R(3)((23*PI/24))]), T(1)((-100))]), CUBOID]))([200, 100, 100])]))

if debug_tower:
	VIEW(Wall_B_Ottusangle)


# =======================================
# TopTower
# =======================================

def Wall_B_Hole (Wall_B_Hole_arg_):
	R2 , W = Wall_B_Hole_arg_
	return (T([1, 2])([2.45*ScaleFactor, 0]))(((COMP([COMP([R(2)(PI/-2.0), S(3)(2)]), T(3)((W/-2.0))]))((RAISE(DIFF)([CYLINDER([R2, W*2.0])(24),(COMP([T(2)((RAISE(DIFF)(R2))), CUBOID]))([R2, 2*R2, W])])))))

TopTower = STRUCT([SecondColumnRing, Cap, T(3)((WallHeight/5.0)), Terrace])


if debug_tower:
	lab.view(TopTower)


# =======================================
# Tooth
# =======================================

def tooth_width (DR):
	return RAISE(SUM)([RAISE(DIFF)([ExternalWallRadius,InternalWallRadius]),DR])


def tooth_mymap1 (tooth_mymap1_arg_):
	DR , H = tooth_mymap1_arg_
	return MAP([RAISE(PROD)([(RAISE(SUM)([S2,S3])),COMP([COS, S1])]), RAISE(PROD)([(RAISE(SUM)([S2,S3])),COMP([SIN, S1])]), S3])((RAISE(PROD)([RAISE(PROD)([INTERVALS((PI/106))(1),T(1)((InternalWallRadius))((INTERVALS((tooth_width(DR)))(1)))]),INTERVALS(H)(1)])))



def Tooth_MyMap2 (Tooth_MyMap2_arg_):
	DR , H = Tooth_MyMap2_arg_
	return MAP([RAISE(PROD)([(S2),(COMP([COS, S1]))]), RAISE(PROD)([(S2),(COMP([SIN, S1]))]), S3])((RAISE(PROD)([RAISE(PROD)([INTERVALS((PI/106))(1),T(1)((InternalWallRadius))((INTERVALS((tooth_width(DR)))(1)))]),INTERVALS(H)(1)])))


def buildTooth():
	RAGGIO = ExternalWallRadius
	LUNGO = TOP([tooth_mymap1([0.0, 0.1]),Tooth_MyMap2([0.1, 0.1])])
	CORTO = Tooth_MyMap2([-0.05, 0.2])
	return STRUCT([LUNGO, R(3)((PI/106)), CORTO])

Tooth = buildTooth()

if debug_tower:
	lab.view(Tooth)


# =======================================
# Plateau
# =======================================


Plateau = (COMP([COMP([OPTIMIZE, STRUCT]), DOUBLE_DIESIS(106)]))([Tooth, R(3)((2*PI/106))])

if debug_tower:
	lab.view(Plateau)

BeltColumnRing = STRUCT([(
		COMP([STRUCT, DOUBLE_DIESIS(6)]))([
			Column_B, Arc_2_b, 
			R(3)(PI/9), 
			Column_B, 
			Arc_2_b, 
			R(3)(PI/9), 
			Arc_2_b, 
			R(3)(PI/9)]),
			T(3)(5.75)(Plateau)
    ])

if debug_tower:
	lab.view(BeltColumnRing)


# =======================================
# BeltWalls
# =======================================


def MyRing (ANGLE):
	def MYRING1 (MYRING1_arg_1):
		R1 , R2 = MYRING1_arg_1
		def MYRING0 (MYRING0_arg_0):
			N , M = MYRING0_arg_0
			domain = T(2)(R1)((RAISE(PROD)([INTERVALS(ANGLE)(N),INTERVALS(R2-R1)(M)])))
			ret_val = MAP(CONS([RAISE(PROD)([S2,COMP([COS, S1])]), RAISE(PROD)([S2,COMP([SIN, S1])])]))(domain)
			return ret_val
		return MYRING0
	
	return MYRING1


BeltWalls = RAISE(PROD)([MyRing(3*PI/9)([InternalWallRadius, ExternalWallRadius*6.0/7.0])([6, 1]),Q(5.75)])

if debug_tower:
	lab.view(BeltWalls)

# =======================================
# SmallWindow1
# =======================================


SmallWindow1 = PROD([MyRing(3*PI/(18*4))([InternalWallRadius-1, (ExternalWallRadius*6.0/7+1)])([2, 1]),Q(1.75)])

if debug_tower:
	lab.view(SmallWindow1)



SmallWindow2 = PROD([
		MyRing(4*PI/(18*5)+PI/64)([InternalWallRadius-1, (ExternalWallRadius*6.0/7+1)])([2, 1]),
		QUOTE([-1.75, -0.35, 2])])

if debug_tower:
	lab.view(SmallWindow2)

# =======================================
# Window3
# =======================================


def Hole3 (ANGLE):
	def HOLE30 (HOLE30_arg_0):
		R1 , R2 = HOLE30_arg_0
		C1 = BEZIER(S1)(LINE1)
		LINE1 = [[R1, 0, 0], [R2, 0, 0]]
		C2 = BEZIER(S1)(LINE2)
		LINE2 = AA((COMP([COMP([UK, R(3)(ANGLE)]), MK])))(LINE1)
		T1 = BEZIER(S1)([[0, 0, 2], [0, 0, 4]])
		T2 = BEZIER(S1)([[0, 0, -2], [0, 0, -4]])
		ret_val = MAP((BEZIER(S3)((CONS([Hole3_Portal1((ANGLE)), Hole3_Portal2((ANGLE))])([R1, R2])))))((PROD([PROD([INTERVALS(1)(1),INTERVALS(1)(12)]),INTERVALS(1)(1)])))
		return ret_val
	return HOLE30

def Hole3_Portal1 (ANGLE):
	def Hole3_Portal10 (Hole3_Portal10_arg_0):
		R1 , R2 = Hole3_Portal10_arg_0
		return CUBICHERMITE(S2)([C1, C2, T1, T2])
	return Hole3_Portal10

def Hole3_Portal2 (ANGLE):
	def Hole3_Portal20 (Hole3_Portal20_arg_0):
		R1 , R2 = Hole3_Portal20_arg_0
		return VECTSUM([BEZIER(S2)([C1, C2]),[K(0), K(0), K(-0.1)]])
	
	return Hole3_Portal20


Window3 = PROD([MyRing((2*PI/9-0.2))([InternalWallRadius-1, (ExternalWallRadius*6.0/7+1)])([1, 1]),Q(2.5)])


if debug_tower:
	lab.view(Window3)



# =======================================
# SectorWall
# =======================================


SectorWall = RAISE(DIFF)([BeltWalls, R(3)((3*PI/(18*5)))(SmallWindow1), R(3)((PI/36))(SmallWindow2), R(3)((PI/9+0.1))(Window3)])


if debug_tower:
	lab.view(SectorWall)



# =======================================
# BeltTower
# =======================================

BeltTower = STRUCT([(COMP([STRUCT, DOUBLE_DIESIS(6)]))([SectorWall, R(3)((PI/3))]),BeltColumnRing])


if debug_tower:
	lab.view(BeltTower)


# =======================================
# Fabric
# =======================================


Fabric = STRUCT([
		T(3)((RAISE(DIFF)(BasementHeight)))(Basement), 
		Steps, 
		FirstFloor, 
		T(3)(FirstFloorHeight)(Kernel), 
		FirstColumnRing, 
		T(3)((RAISE(DIFF)([FirstFloorHeight,(0.095*ScaleFactor)]))), 
		Terrace, (
		COMP([STRUCT, DOUBLE_DIESIS(5)]))([
			SecondColumnRing, 
			T(3)((WallHeight/5.0)), 
			Terrace
		]), 
		T(3)(WallHeight), 
		TowerCap, 
		TopTower, 
		T(3)((RAISE(DIFF)([MAX(3)(TowerCap),0.3]))), 
		BeltTower
	])

out = Fabric

#Plasm.save(out,':models/pisa.hpc.gz')
print "Pisa evaluated in", time.clock() - start, "seconds."
lab.view(out)

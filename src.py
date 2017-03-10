import vtk
from vtk.util.colors import brown_ochre, tomato, banana,chocolate,turquoise,blue_medium

#Reading the fohe file
fohe = vtk.vtkBYUReader()
fohe.SetGeometryFileName("fohe.g")
fohe.Update()

#Calculating the normals
normals = vtk.vtkPolyDataNormals()
normals.SetInputConnection(fohe.GetOutputPort())



#Construction and Locating the plane
plane = vtk.vtkPlane()
plane.SetOrigin(fohe.GetOutput().GetCenter())
plane.SetNormal(1, 0, 1)




#Function for displaying the clipping planes
sampler = vtk.vtkSampleFunction()
sampler.SetImplicitFunction(plane)
sampler.SetModelBounds(fohe.GetOutput().GetBounds())
contour = vtk.vtkContourFilter()
contour.SetInputConnection(sampler.GetOutputPort())
contour.SetValue(0, 0.0)


planeActor = vtk.vtkActor()
planeMapper = vtk.vtkPolyDataMapper()
planeMapper.SetInputConnection(contour.GetOutputPort())
planeActor.SetMapper(planeMapper)
planeActor.GetProperty().SetColor(banana)
planeActor.GetProperty().SetOpacity(0.2)


#Creating the clipper
clipper = vtk.vtkClipPolyData()
clipper.SetInputConnection(normals.GetOutputPort())
clipper.SetClipFunction(plane)
clipper.GenerateClippedOutputOn()
clipper.SetValue(0)
clipper.Update()

clipMapper = vtk.vtkPolyDataMapper()
clipMapper.SetInputConnection(clipper.GetOutputPort())
clipMapper.ScalarVisibilityOff()
clipMapper.Update()



backProp = vtk.vtkProperty()
backProp.SetDiffuseColor(tomato)
clipActor = vtk.vtkActor()
clipActor.SetMapper(clipMapper)
clipActor.GetProperty().SetColor(banana)
clipActor.SetBackfaceProperty(backProp)
clipActor.GetProperty().SetOpacity(0.9)


#creation of the function for intersection area between the plane and polygon data
cutEdges = vtk.vtkCutter()
cutEdges.SetInputConnection(normals.GetOutputPort())
cutEdges.SetCutFunction(plane)
cutEdges.GenerateCutScalarsOn()
cutEdges.SetValue(0,0)
cutEdges.Update()
cutStrips = vtk.vtkStripper()
cutStrips.SetInputConnection(cutEdges.GetOutputPort())
cutStrips.Update()
cutPoly = vtk.vtkPolyData()
cutPoly.SetPoints(cutStrips.GetOutput().GetPoints())
cutPoly.SetPolys(cutStrips.GetOutput().GetLines())

cutTriangles = vtk.vtkTriangleFilter()
cutTriangles.SetInputData(cutPoly)
cutTriangles.Update()
cutMapper = vtk.vtkPolyDataMapper()
cutMapper.SetInputData(cutPoly)
cutMapper.SetInputConnection(cutTriangles.GetOutputPort())
cutMapper.Update()
cutActor = vtk.vtkActor()
cutActor.SetMapper(cutMapper)
cutActor.GetProperty().SetColor(0.5412, 0.1686, 0.8863)
cutActor.GetProperty().SetOpacity(0.9)

restMapper = vtk.vtkPolyDataMapper()
restMapper.SetInputData(clipper.GetClippedOutput())
restMapper.Update()
restActor = vtk.vtkActor()
restActor.SetMapper(restMapper)
restActor.GetProperty().SetRepresentationToWireframe()



ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)

# Create a renderwindowinteractor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Assign actors to the renderer
ren.AddActor(clipActor)
ren.AddActor(cutActor)
ren.AddActor(restActor)
ren.AddActor(planeActor)

renWin.Render()
 

#converting to jpeg file format
w2if = vtk.vtkWindowToImageFilter()
w2if.SetInput(renWin)
w2if.Update()
 
writer = vtk.vtkJPEGWriter()
writer.SetFileName("assignment2.jpeg")
writer.SetInputConnection(w2if.GetOutputPort())
writer.Write()


# Enable user interface interactor
iren.Initialize()
iren.Start()

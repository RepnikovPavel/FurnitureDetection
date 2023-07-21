using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

[System.Serializable]
public class category_cortege{
    public string supercategory;
    public int id;
    public string name;
}

[System.Serializable]
public class image_cortage{
    public string file_name;
    public int height;
    public int width;
    public int id;
}

[System.Serializable]
public class annotation_cortege{
    public int image_id;
    public float[] bbox;
    public int category_id;
    public int id;
}


[System.Serializable]
public class COCODatasetAnnotation{
    public List<category_cortege> categories = new List<category_cortege>();
    public List<image_cortage> images = new List<image_cortage>();
    public List<annotation_cortege> annotations = new List<annotation_cortege>();
}

public class MoveAroundObject : MonoBehaviour
{
    // [SerializeField]
    // private float _mouseSensitivity = 3.0f;

    // private float _rotationY;
    // private float _rotationX;

    // [SerializeField]
    // private Transform _target;

    // [SerializeField]
    // private float _distanceFromTarget = 3.0f;

    // private Vector3 _currentRotation;
    // private Vector3 _smoothVelocity = Vector3.zero;

    // [SerializeField]
    // private float _smoothTime = 0.2f;

    // [SerializeField]
    // private Vector2 _rotationXMinMax = new Vector2(-40, 40);

    // public GameObject player;

    public GameObject spawner;

    private Dictionary<int, GameObject> Objs;
    private Dictionary<int,BBOX> ObjsBoxes;

    private Spawner spawnercomp;

    private float[] camerabox;

    private Vector3[] CameraPositions;
    private Vector3[] CameraDirections;
    private int CurrentCamereState;

    Camera camera;

    COCODatasetAnnotation dataset;
    private int CurrentImageId;
    private int CurrentAnnotationId;

    public int number_of_images_;

    private Coroutine coroutine_;
    
    void Start(){
        
        CurrentCamereState =0;
        CurrentImageId=0;
        CurrentAnnotationId=0;
        camerabox = new float[]{-5.4f, 5.4f, 0.5f, 2.0f, -5.4f, 5.4f};
        // camerabox = new float[]{-5.4f, 5.4f, 10.0f, 20.0f, -5.4f, 5.4f};

        camera = Camera.main;
        spawnercomp = spawner.GetComponent("Spawner") as Spawner;

        // USING spawner as namespace
        spawnercomp.InitDictWithPrefabs();
        spawnercomp.LoadFurniturePrefabs();



        // spawnercomp.LoadFurniturePrefabs();
        // // spawnercomp.CreateObjectsInScene();
        // spawnercomp.CreateLightInScene();
        // while(true){
        //     if(spawnercomp.IsStartEnd){
        //         break;
        //     }
        // }
        // Debug.Log("start is over");

        // CREATE directory with dataset
        if(!Directory.Exists(Application.dataPath+"/DATASET")){
            Directory.CreateDirectory(Application.dataPath+"/DATASET");
        }
        if(!Directory.Exists(Application.dataPath+"/DATASET/IMAGES")){
            Directory.CreateDirectory(Application.dataPath+"/DATASET/IMAGES");
        }
        if(!Directory.Exists(Application.dataPath+"/DATASET/ANNOTATIONS")){
            Directory.CreateDirectory(Application.dataPath+"/DATASET/ANNOTATIONS");
        }
        ClearDir(Application.dataPath+"/DATASET/IMAGES");
        ClearDir(Application.dataPath+"/DATASET/ANNOTATIONS");

        // Debug.Log("before store categories");
        // CREATE datset annotation
        dataset = new COCODatasetAnnotation();
        // FILL categories to dataset
        // Debug.Log(spawnercomp.PrefabCategory);
        // Debug.Log(spawnercomp.PrefabCategory.Count);
        foreach(var pair in spawnercomp.Categories){
            // Debug.Log(i.ToString("R"));
            var category_id = pair.Value;
            var category_name_ = pair.Key;
            dataset.categories.Add(new category_cortege(){supercategory="furniture",id=category_id,name=category_name_});
        }
        // Debug.Log("after store categories");

        // SET camera position to object spawner position
        camera.transform.position = spawner.transform.position;
        camera.transform.eulerAngles = spawner.transform.eulerAngles;
        // Debug.Log(camerabox[0].ToString("R"));
        // Debug.Log(camerabox);

        // SET camera pisition and directions                                                                                                                                                                                                                           
                                                                                                                                          
        var ax = camerabox[0];                                                                                                                                                                                                                                                                                                                                                                                           
        var bx = camerabox[1];                                                                                                                                                                                                                                                                                                                                                                                           
        var ay = camerabox[2];                                                                                                                                                                                                                                                                                                                                                                                           
        var by = camerabox[3];                                                                                                                                                                                                                                                                                                                                                                                           
        var az = camerabox[4];                                                                                                                                                                                                                                                                                                                                                                                           
        var bz = camerabox[5];                                                                                                                                                                                                                                                                                                                                                                                           
        var p1 = camera.transform.position + new Vector3(ax,ay,az);
        var p2 = camera.transform.position + new Vector3(bx,ay,az);
        var p3 = camera.transform.position + new Vector3(bx,ay,bz);
        var p4 = camera.transform.position + new Vector3(ax,ay,bz);
        var p5 = camera.transform.position + new Vector3(ax,by,az);
        var p6 = camera.transform.position + new Vector3(bx,by,az);
        var p7 = camera.transform.position + new Vector3(bx,by,bz);
        var p8 = camera.transform.position + new Vector3(ax,by,bz);
        Vector3[] positions = new Vector3[]{
            p1,
            p2,
            p3,
            p4,
            p5,
            p6,
            p7,
            p8
        };
        Vector3[] directions = new Vector3[]{
            p7-p1,
            p8-p2,
            p5-p3,
            p6-p4,
            p3-p5,
            p4-p6,
            p1-p7,
            p2-p8
        };
        for(var i =0;i < directions.Length;i++){
            directions[i].Normalize();
        }
        CameraPositions = positions;
        CameraDirections = directions;

        // minima number of images 
        // number_of_images_ = spawnercomp.PrefabsNames.Length*CameraPositions.Length;
        number_of_images_ = Mathf.Max(1000,spawnercomp.PrefabsNames.Length*CameraPositions.Length);
        // number_of_images_ = 1000;
        Cursor.visible = false;
        // coroutine_ = WriteImg_();
        coroutine_ = StartCoroutine(WriteImg_());
    }
    void MakeNextImage() {
        if(CurrentImageId>=number_of_images_){
                Debug.Log("images are recorded");
                Debug.Log("recording annotations ...");
                File.WriteAllText(Application.dataPath + "/DATASET/ANNOTATIONS/annotations.json",JsonUtility.ToJson(dataset));
                Debug.Log("annotations are recorded");
                Debug.Log("all data are corded to"+ Application.dataPath + "/DATASET/");
            return;
        }
        else{
            // it seems that stop coroutine not free memory anyway
            StopCoroutine("WriteImg_");
            coroutine_ = StartCoroutine(WriteImg_());
        }

    }   
    void Update()
    {
        // if(CurrentImageId<number_of_images_){
        //     WriteImg_();
        // }
        // if(CurrentImageId==number_of_images_){
        //     Debug.Log("images are recorded");
        //     Debug.Log("recording annotations ...");
        //     File.WriteAllText(Application.dataPath + "/DATASET/ANNOTATIONS/annotations.json",JsonUtility.ToJson(dataset));
        //     Debug.Log("annotations are recorded");

        //     CurrentImageId+=1;
        // }
    }

    void ClearDir(string path){
        System.IO.DirectoryInfo di = new DirectoryInfo(path);
        foreach (FileInfo file in di.GetFiles())
        {
            file.Delete(); 
        }
        foreach (DirectoryInfo dir in di.GetDirectories())
        {
            dir.Delete(true); 
        }

    }
    bool IsAInsideB(Rect A, Rect B){
        // if A and B equal return 1
        var Axld = A.x;
        var Ayld = A.y;
        var Bxld = B.x;
        var Byld = B.y;

        var Axtr = A.x + A.width;
        var Aytr = A.y + A.height;
        var Bxtr = B.x + B.width;
        var Bytr = B.y + B.height;

        if((Axld >= Bxld ) && (Ayld >= Byld)  && (Axtr <= Bxtr ) && (Aytr <= Bytr)){
            return true;
        }
        else{
            return false;
        }

    }
    // IEnumerator WriteImg(){
        // yield return WriteImg_();
    // }

    IEnumerator WriteImg_(){
        Debug.Log("{"+CurrentImageId.ToString()+"}/{"+number_of_images_.ToString()+"}");
        // Debug.Log("write img call");
        // MOVE camera

        // if (Input.GetKeyDown("r"))
        // {
            // Debug.Log("key pressed");
        // NextCameraState();
        // }
        PrepareScene();


        // COMPUTE bboxes 
        Objs = spawnercomp.Objs;
        ObjsBoxes = spawnercomp.ObjsBoxes;

        var ObjRects = new Dictionary<int, Rect>();
        var ObjZ = new Dictionary<int, float>();
        // Debug.Log(ObjsBoxes);
        // Debug.Log(spawnercomp);
        foreach(var pair in ObjsBoxes){
            var objid_=  pair.Key;
            var box_ = pair.Value;
            // Debug.Log(box_);
            var rect_ = box_.GetBoxIfInCameraView();
            // Debug.Log(rect_);
            if(rect_.width>=0.0f){
                ObjRects.Add(objid_,rect_);
                ObjZ.Add(objid_,box_.CurrentZ);
            }
        }
        var all_ids_ = ObjRects.Keys;
        var ToDatsetIds = new List<int>();
        foreach(var objid in all_ids_){
            // is the current bbox nested in others?
            // if yes, and it is further away from the camera, then you do not need to draw or record it
            bool IsNotInside = true;
            foreach(var anotherid in all_ids_){
                if(objid == anotherid){
                    continue;
                }
                var isinside = IsAInsideB(ObjRects[objid],ObjRects[anotherid]);
                // Debug.Log(isinside);
                // Debug.Log(ObjZ[objid]);
                if( isinside && (ObjZ[objid]>ObjZ[anotherid])){
                    IsNotInside = false;
                    ObjsBoxes[objid].DoINeedToDrawRect = false;
                    break;
                }

            }
            if(IsNotInside){
                ToDatsetIds.Add(objid);
            }

        }

        // rendering step
        foreach(var objid in ToDatsetIds){
            // Debug.Log(objid);
            var obj_ = ObjsBoxes[objid];
            // obj_.DoINeedToDrawRect = true;
            obj_.DoINeedToDrawRect = false;

        }
        // if ToDatsetIds.Count ==0 then there are no boxes - camera is set in wrong position or direction
        if(ToDatsetIds.Count!=0){

            // store annotations to dataset
            foreach(var objid in ToDatsetIds){
                // Debug.Log(objid);
                var obj_ = ObjsBoxes[objid];
                var rect_ = XldYldWH_TO_XtlYtlWH(ObjRects[objid]);
                var category_name = obj_.category;
                // Debug.Log(category_name);
                float[] bbox = new float[]{rect_.x,rect_.y,rect_.width,rect_.height};
                var category_id =  spawnercomp.Categories[category_name];
                // Debug.Log(category_id);
                dataset.annotations.Add(new annotation_cortege(){
                    image_id = CurrentImageId,
                    bbox= bbox,
                    category_id = category_id,
                    id = CurrentAnnotationId
                });
                CurrentAnnotationId +=1;
            }
            // Debug.Log("before wait for end of frame");
            yield return new WaitForEndOfFrame();
            // Debug.Log("after wait for end of frame");

            // STORE image to dataset

            // Debug.Log("after wair end of frame");
            // Debug.Log("write img call");
            var viewport_rect = camera.pixelRect;
            int width = (int)viewport_rect.width;
            int height = (int)viewport_rect.height;

            Texture2D tex = new Texture2D(width, height, TextureFormat.RGB24, false);
            tex.ReadPixels(new Rect(0, 0, width, height), 0, 0);
            tex.Apply();
            
            byte[] pngbytes = ImageConversion.EncodeToPNG(tex);
            // Debug.Log("before create image name");
            var img_name_ = "_"+CurrentImageId.ToString()+".png";
            // Debug.Log(img_name_);
            // Debug.Log("before write to disk");

            dataset.images.Add(new image_cortage(){
                file_name =img_name_,
                height = height,
                width = width,
                id = CurrentImageId
            });

            File.WriteAllBytes(path: Application.dataPath+"/DATASET/IMAGES/"+img_name_,bytes: pngbytes);
            CurrentImageId+=1;
            Debug.Log("image is recorded");
        }
        MakeNextImage();
    }

    Rect XldYldWH_TO_XtlYtlWH(Rect rect){
        var viewport_rect= camera.pixelRect;
        return new Rect(rect.x,viewport_rect.height-rect.y-rect.height,rect.width,rect.height);
    }
    Texture2D toTexture2D(RenderTexture rTex, int width, int height)
    {
        Texture2D tex = new Texture2D(width, height, TextureFormat.ARGB32, false);
        // ReadPixels looks at the active RenderTexture.
        RenderTexture.active = rTex;
        tex.ReadPixels(new Rect(0, 0, rTex.width, rTex.height), 0, 0);
        tex.Apply();
        return tex;
    }

    void NextCameraState(){
        // Debug.Log("next camera state call");
        if(CurrentCamereState>= CameraPositions.Length){
            CurrentCamereState =0;
        }
        camera.transform.position = CameraPositions[CurrentCamereState];
        camera.transform.forward = CameraDirections[CurrentCamereState];
        // Debug.Log(camera.transform.localPosition);
        CurrentCamereState +=1;
    }

    void NextSceneState(){
        // CALL before call NextCameraState()
        // Debug.Log("before change state");
        spawnercomp.ChangeStateOfScene(CurrentCamereState, CameraPositions.Length);
        // Debug.Log("after cnage state of scene");
    }

    void PrepareScene(){
        NextSceneState();
        NextCameraState();
    }

    // public void DrawBox(Vector3 pos, Quaternion rot, Vector3 scale, Color c)
    // {
    //     // create matrix
    //     Matrix4x4 m = new Matrix4x4();
    //     m.SetTRS(pos, rot, scale);

    //     var point1 = m.MultiplyPoint(new Vector3(-0.5f, -0.5f, 0.5f));
    //     var point2 = m.MultiplyPoint(new Vector3(0.5f, -0.5f, 0.5f));
    //     var point3 = m.MultiplyPoint(new Vector3(0.5f, -0.5f, -0.5f));
    //     var point4 = m.MultiplyPoint(new Vector3(-0.5f, -0.5f, -0.5f));

    //     var point5 = m.MultiplyPoint(new Vector3(-0.5f, 0.5f, 0.5f));
    //     var point6 = m.MultiplyPoint(new Vector3(0.5f, 0.5f, 0.5f));
    //     var point7 = m.MultiplyPoint(new Vector3(0.5f, 0.5f, -0.5f));
    //     var point8 = m.MultiplyPoint(new Vector3(-0.5f, 0.5f, -0.5f));

    //     Debug.DrawLine(point1, point2, c);
    //     Debug.DrawLine(point2, point3, c);
    //     Debug.DrawLine(point3, point4, c);
    //     Debug.DrawLine(point4, point1, c);

    //     Debug.DrawLine(point5, point6, c);
    //     Debug.DrawLine(point6, point7, c);
    //     Debug.DrawLine(point7, point8, c);
    //     Debug.DrawLine(point8, point5, c);

    //     Debug.DrawLine(point1, point5, c);
    //     Debug.DrawLine(point2, point6, c);
    //     Debug.DrawLine(point3, point7, c);
    //     Debug.DrawLine(point4, point8, c);

    //     // // optional axis display
    //     // Debug.DrawRay(m.GetPosition(), m.GetForward(), Color.magenta);
    //     // Debug.DrawRay(m.GetPosition(), m.GetUp(), Color.yellow);
    //     // Debug.DrawRay(m.GetPosition(), m.GetRight(), Color.red);
    // }
}
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class MoveAroundObject : MonoBehaviour
{
    [SerializeField]
    private float _mouseSensitivity = 3.0f;

    private float _rotationY;
    private float _rotationX;

    [SerializeField]
    private Transform _target;

    [SerializeField]
    private float _distanceFromTarget = 3.0f;

    private Vector3 _currentRotation;
    private Vector3 _smoothVelocity = Vector3.zero;

    [SerializeField]
    private float _smoothTime = 0.2f;

    [SerializeField]
    private Vector2 _rotationXMinMax = new Vector2(-40, 40);

    public GameObject player;

    public GameObject spawner;

    private Dictionary<int, GameObject> Objs;
    private Dictionary<int,BBOX> ObjsBoxes;

    private Spawner spawnercomp;

    Camera camera;
    IEnumerator Start(){
        camera = Camera.main;
        spawnercomp = spawner.GetComponent("Spawner") as Spawner;

        while (true){
            yield return WriteImg_();
        }
    }
    void Update()
    {
        float mouseX = Input.GetAxis("Mouse X") * _mouseSensitivity;
        float mouseY = Input.GetAxis("Mouse Y") * _mouseSensitivity * (-1.0f);

        _rotationY += mouseX;
        _rotationX += mouseY;

        // Apply clamping for x rotation 
        _rotationX = Mathf.Clamp(_rotationX, _rotationXMinMax.x, _rotationXMinMax.y);

        Vector3 nextRotation = new Vector3(_rotationX, _rotationY);

        // Apply damping between rotation changes
        _currentRotation = Vector3.SmoothDamp(_currentRotation, nextRotation, ref _smoothVelocity, _smoothTime);
        transform.localEulerAngles = _currentRotation;

        // Substract forward vector of the GameObject to point its forward vector to the target
        transform.position = _target.position - transform.forward * _distanceFromTarget;
        // save screen texture to png 
        
        Objs = spawnercomp.Objs;
        ObjsBoxes = spawnercomp.ObjsBoxes;

        // calc bboxes 
        var ObjRects = new Dictionary<int, Rect>();
        var ObjZ = new Dictionary<int, float>();
        // Debug.Log(ObjsBoxes);
        // Debug.Log(spawnercomp);
        foreach(var pair in ObjsBoxes){
            var objid_=  pair.Key;
            var box_ = pair.Value;
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
                if(IsAInsideB(ObjRects[objid],ObjRects[anotherid]) && (ObjZ[objid]>ObjZ[anotherid])){
                    IsNotInside = false;
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
            obj_.DoINeedToDrawRect = true;
        }

        // store to dataset


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
        yield return new WaitForEndOfFrame();
        // Debug.Log("write img call");
        var viewport_rect = camera.pixelRect;
        int width = (int)viewport_rect.width;
        int height = (int)viewport_rect.height;

        Texture2D tex = new Texture2D(width, height, TextureFormat.RGB24, false);
        tex.ReadPixels(new Rect(0, 0, width, height), 0, 0);
        tex.Apply();
        byte[] pngbytes = ImageConversion.EncodeToPNG(tex);
        File.WriteAllBytes(path: "/home/user/tmp/tmp_img.png",bytes: pngbytes);

        // 
        // camera.targetTexture = scrRenderTexture;
        // camera.Render();
        // camera.targetTexture = camRenderTexture;
// 
        // RenderTexture.active = scrRenderTexture;
        // scrTexture.ReadPixels(new Rect(0, 0, scrTexture.width, scrTexture.height), 0, 0);
        // scrTexture.Apply();
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
}
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;
public class BBOX : MonoBehaviour
{

    Camera camera;
    MeshRenderer meshrenderer;
    Plane[] cameraFrustum;
    Collider collider;
    Renderer renderer;

    Rect CurrentRect = new Rect();
    public bool DoINeedToDrawRect;

    public float CurrentZ;

    public string category;
    public int object_id;

    void Start()
    {
        // camera = Camera.main;
        // meshrenderer = GetComponent<MeshRenderer>();
        // Debug.Log("in bbox script start");
        // collider = GetComponent<Collider>();
        // // renderer = GetComponent<Renderer>();
        // Debug.Log(collider);
        // Debug.Log(renderer);
        // Debug.Log("after get collider and renderer");
        
    }

    // Update is called once per frame
    void Update()
    {
        // Debug.Log(category);
        // Debug.Log(object_id);
        // var bounds = collider.bounds;
        // cameraFrustum = GeometryUtility.CalculateFrustumPlanes(camera);
        // if (GeometryUtility.TestPlanesAABB(cameraFrustum,bounds)){
        //     // meshrenderer.material.color = Color.green;
        //     CurrentRect = GetBBox();
        //     // Debug.Log(CurrentRect);
        //     DoINeedToDrawRect = true;
        //     // Debug.Log(CurrentRect);
        //     // Debug.Log("green");
        // } else {
        //     // renderer.sharedMaterial.color = Color.red;
        //     // meshrenderer.material.color = Color.red;
        //     DoINeedToDrawRect = false;
        //     // Debug.Log("red");
        // }


        // Debug.Log(rect);
        // GUIDrawRect(rect,Color.red);

    }

    public Rect GetBoxIfInCameraView(){
        // return width< 0.0f if not in camera view
                // Debug.Log(category);
        // Debug.Log(object_id);
        // Debug.Log(camera);

        camera = Camera.main;
        meshrenderer = GetComponent<MeshRenderer>();
        Debug.Log("in bbox script start");
        collider = GetComponent<Collider>();
        renderer = GetComponent<Renderer>();


        Debug.Log("before get collider");
        var bounds = collider.bounds;
        Debug.Log("after get collider");
        Debug.Log(collider);
        Debug.Log(bounds);
        cameraFrustum = GeometryUtility.CalculateFrustumPlanes(camera);
        // Debug.Log(cameraFrustum);
        bool IsInCameraView = GeometryUtility.TestPlanesAABB(cameraFrustum,bounds);
        // Debug.Log(IsInCameraView);
        if (IsInCameraView){
            // meshrenderer.material.color = Color.green;
            CurrentRect = GetBBox();
            // Debug.Log(CurrentRect);
            // Debug.Log(CurrentRect);
            DoINeedToDrawRect = true;
            // Debug.Log(CurrentRect);
            // Debug.Log("green");
            return CurrentRect;
        } else {
            // renderer.sharedMaterial.color = Color.red;
            // meshrenderer.material.color = Color.red;
            DoINeedToDrawRect = false;
            CurrentRect.width = -1.0f;
            return CurrentRect;
            // Debug.Log("red");
        }


        // Debug.Log(rect);
        // GUIDrawRect(rect,Color.red);
    }

    public float GetZInCameraView(){
        return CurrentZ;
    }


    void OnGUI(){
        if(DoINeedToDrawRect){
            GUIDrawRect(CurrentRect,Color.red);
        }
    }

    // public static Rect GetBBox(GameObject go)
    private Rect GetBBox()
    {
        // 
        // Debug.Log("get box call");

        // Vector3 cen = go.GetComponent<Renderer>().bounds.center;
        // Vector3 ext = go.GetComponent<Renderer>().bounds.extents;
        var r = GetComponent<Renderer>();
        Vector3 cen = r.bounds.center;
        Vector3 ext = r.bounds.extents;
        // Debug.Log(r);
        // Debug.Log(cen);
        // Debug.Log(ext);
        // Vector2[] extentPoints = new Vector2[8]
        // {
        //     HandleUtility.WorldToGUIPoint(new Vector3(cen.x-ext.x, cen.y-ext.y, cen.z-ext.z)),
        //     HandleUtility.WorldToGUIPoint(new Vector3(cen.x+ext.x, cen.y-ext.y, cen.z-ext.z)),
        //     HandleUtility.WorldToGUIPoint(new Vector3(cen.x-ext.x, cen.y-ext.y, cen.z+ext.z)),
        //     HandleUtility.WorldToGUIPoint(new Vector3(cen.x+ext.x, cen.y-ext.y, cen.z+ext.z)),
        //     HandleUtility.WorldToGUIPoint(new Vector3(cen.x-ext.x, cen.y+ext.y, cen.z-ext.z)),
        //     HandleUtility.WorldToGUIPoint(new Vector3(cen.x+ext.x, cen.y+ext.y, cen.z-ext.z)),
        //     HandleUtility.WorldToGUIPoint(new Vector3(cen.x-ext.x, cen.y+ext.y, cen.z+ext.z)),
        //     HandleUtility.WorldToGUIPoint(new Vector3(cen.x+ext.x, cen.y+ext.y, cen.z+ext.z))
        // };
        var on_screen_with_depth1 = camera.WorldToScreenPoint(new Vector3(cen.x-ext.x, cen.y-ext.y, cen.z-ext.z));
        var on_screen_with_depth2 = camera.WorldToScreenPoint(new Vector3(cen.x+ext.x, cen.y-ext.y, cen.z-ext.z));
        var on_screen_with_depth3 = camera.WorldToScreenPoint(new Vector3(cen.x-ext.x, cen.y-ext.y, cen.z+ext.z));
        var on_screen_with_depth4 = camera.WorldToScreenPoint(new Vector3(cen.x+ext.x, cen.y-ext.y, cen.z+ext.z));
        var on_screen_with_depth5 = camera.WorldToScreenPoint(new Vector3(cen.x-ext.x, cen.y+ext.y, cen.z-ext.z));
        var on_screen_with_depth6 = camera.WorldToScreenPoint(new Vector3(cen.x+ext.x, cen.y+ext.y, cen.z-ext.z));
        var on_screen_with_depth7 = camera.WorldToScreenPoint(new Vector3(cen.x-ext.x, cen.y+ext.y, cen.z+ext.z));
        var on_screen_with_depth8 = camera.WorldToScreenPoint(new Vector3(cen.x+ext.x, cen.y+ext.y, cen.z+ext.z));
        // Debug.Log(on_screen_with_depth1);
        // for z y can get any of coords if y use box collider
        // else y need get nearest point to camera
        float[] zarr = new float[]{
            on_screen_with_depth1[2],
            on_screen_with_depth2[2],
            on_screen_with_depth3[2],
            on_screen_with_depth4[2],
            on_screen_with_depth5[2],
            on_screen_with_depth6[2],
            on_screen_with_depth7[2],
            on_screen_with_depth8[2]

        };
        // Debug.Log(zarr);
        CurrentZ = on_screen_with_depth1[2];
        for(var i=0;i<8;i++){
            CurrentZ = Mathf.Min(CurrentZ,zarr[i]);
        }
        // string mes = CurrentZ.ToString("R");
        // Debug.Log(mes);

        Vector2[] extentPoints = new Vector2[8]
        {
            new Vector2(on_screen_with_depth1[0],on_screen_with_depth1[1]),
            new Vector2(on_screen_with_depth2[0],on_screen_with_depth2[1]),
            new Vector2(on_screen_with_depth3[0],on_screen_with_depth3[1]),
            new Vector2(on_screen_with_depth4[0],on_screen_with_depth4[1]),
            new Vector2(on_screen_with_depth5[0],on_screen_with_depth5[1]),
            new Vector2(on_screen_with_depth6[0],on_screen_with_depth6[1]),
            new Vector2(on_screen_with_depth7[0],on_screen_with_depth7[1]),
            new Vector2(on_screen_with_depth8[0],on_screen_with_depth8[1])
        };
        // Debug.Log(extentPoints[0]);
        Vector2 min = extentPoints[0];
        Vector2 max = extentPoints[0];
        foreach (Vector2 v in extentPoints)
        {
            min = Vector2.Min(min, v);
            max = Vector2.Max(max, v);
        }

        // var r = GetComponent<Renderer>();
        // if (r == null)
        //     return new Rect();
        // var bounds = r.bounds;
        // Gizmos.matrix = Matrix4x4.identity;
        // Gizmos.color = Color.blue;
        // Gizmos.DrawWireCube(bounds.center, bounds.extents * 2);
        // Debug.Log(min.x);
        var out_ = new Rect(min.x, min.y, max.x - min.x, max.y - min.y);
        // Debug.Log(out_);
        return out_;
    }
    private static Texture2D _staticRectTexture;
    private static GUIStyle _staticRectStyle;
 
    // Note that this function is only meant to be called from OnGUI() functions.
    public void GUIDrawRect( Rect position, Color color )
    {
        if( _staticRectTexture == null )
        {
            _staticRectTexture = new Texture2D( 1, 1 );
            _staticRectTexture.SetPixel(0, 0, color);
            _staticRectTexture.Apply();
        }
 
        if( _staticRectStyle == null )
        {
            _staticRectStyle = new GUIStyle();
        }
 
        _staticRectTexture.SetPixel( 0, 0, color );
        _staticRectTexture.Apply();
 
        _staticRectStyle.normal.background = _staticRectTexture;
        var viewport_rect= camera.pixelRect;
        Rect tmprect = new Rect(new Vector2(position.x,viewport_rect.height- position.y - position.height),new Vector2(position.width,position.height));
        // Debug.Log(viewport_rect);
        // GUI.Box( tmprect, GUIContent.none, _staticRectStyle );
        // GUI.DrawTexture(,_staticRectTexture);
        var area = tmprect;
        Rect lineArea = area;
        int frameWidth = 2;
        lineArea.height = frameWidth; //Top line
        GUI.DrawTexture(lineArea, _staticRectTexture);
        lineArea.y = area.yMax - frameWidth; //Bottom
        GUI.DrawTexture(lineArea, _staticRectTexture);
        lineArea = area;
        lineArea.width = frameWidth; //Left
        GUI.DrawTexture(lineArea, _staticRectTexture);
        lineArea.x = area.xMax - frameWidth;//Right
        GUI.DrawTexture(lineArea, _staticRectTexture);
 
    }
    public static void DrawRect(Vector3 min, Vector3 max, Color color)
    {
        UnityEngine.Debug.DrawLine(min, new Vector3(min.x, max.y), color);
        UnityEngine.Debug.DrawLine(new Vector3(min.x, max.y), max, color);
        UnityEngine.Debug.DrawLine(max, new Vector3(max.x, min.y), color);
        UnityEngine.Debug.DrawLine(min, new Vector3(max.x, min.y), color);
    }
}

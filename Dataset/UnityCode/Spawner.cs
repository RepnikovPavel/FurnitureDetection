using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using UnityEditor;

public class Spawner : MonoBehaviour
{
    // obj_id object_ref
    public Dictionary<int, GameObject> Objs = new Dictionary<int, GameObject>();
    public Dictionary<int, BBOX> ObjsBoxes = new Dictionary<int, BBOX>();
    // Start is called before the first frame update
    void Start()
    {   

        // var BaseDir = "/home/user/UnityProjects/MakeDataset/Assets/objects";
        var BaseDir = "objects";
        var ObjsURL = new List<string>();
        ObjsURL.Add(Path.Join(BaseDir,"Cube"));
        // Debug.Log("Assets/objects/Cube.prefab");
        // Assets/Resources/Cube.prefab
        // ax bx ay by        
        float[] box = {0.0f, 10.0f, 0.0f, 10.0f};
        int N = 10;

        var prefab = Resources.Load("stool_2") as GameObject;
        // var mesh = prefab.GetComponent<Mesh>();
        // mesh.setM
        // var mesh = Resources.Load("_1") as Mesh;
        // prefab.GetComponent<MeshFilter>().mesh = mesh;
        // Debug.Log(prefab);
        var ObjInScene = Instantiate(prefab);
        var bbox = ObjInScene.GetComponent("BBOX") as BBOX;
        bbox.category = "custom_category_name";
        bbox.object_id = 1;

        // Debug.Log(ObjInScene.transform.position);
        ObjInScene.transform.position = new Vector3(0.0f,-1.3f,0.0f);
        ObjInScene.transform.eulerAngles = new Vector3(0.0f,0.0f,0.0f);
        // Debug.Log(ObjInScene.transform.position);

        var mr = ObjInScene.GetComponent<MeshRenderer>();
        // mr.material.shader = Shader.Find ("Standard");
        // mr.material.SetFloat("_Glossiness", 1.0f);
        mr.material.SetFloat("_GlossMapScale", 1.0f);
        Objs.Add(bbox.object_id, ObjInScene);
        ObjsBoxes.Add(bbox.object_id, bbox);
        
    
    }
    // Update is called once per frame
    void Update()
    {
    }
}

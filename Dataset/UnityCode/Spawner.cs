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

    private Dictionary<string, GameObject> Prefabs= new Dictionary<string, GameObject>();

    float[] placement_area = {-10.0f, 10.0f, -2.0f,-2.0f, -10.0f, 10.0f};


    // Start is called before the first frame update
    void Start()
    {   

        // var BaseDir = "/home/user/UnityProjects/MakeDataset/Assets/objects";
        var BaseDir = "objects";
        var ObjsURL = new List<string>();
        ObjsURL.Add(Path.Join(BaseDir,"Cube"));
        string[] PrefabsNames = new string[]{
            "stool_1",
            "stool_2"
        };
        string[] PrefabCategory = new string[]{
            "stool",
            "stool"
        };

        for(var i=0;i<PrefabsNames.Length;i++){
            var prefab = Resources.Load(PrefabsNames[i]) as GameObject; 
            Prefabs.Add(PrefabsNames[i], prefab);
        }
        int last_id_ = 0;
        int low_ = 0;
        int high_ = PrefabsNames.Length-1;
        int num_of_objects_ = 10;
        // x1 x2 y1 y2 z1 z2


        for(var i =0; i< num_of_objects_;i++){
            int name_pos_ = Mathf.RoundToInt(Random.Range((float)low_,(float)high_));
            var prefab_name_ = PrefabsNames[name_pos_];
            var ObjInScene = Instantiate(Prefabs[prefab_name_]);

            var bbox = ObjInScene.GetComponent("BBOX") as BBOX;
            // SET category name and object in scene id
            bbox.category = PrefabCategory[name_pos_];
            bbox.object_id = last_id_;

            // PLACE object in random position inside box
            var x_ = Random.Range(placement_area[0],placement_area[1]);
            var y_ = Random.Range(placement_area[2],placement_area[3]);
            var z_ = Random.Range(placement_area[4],placement_area[5]);
            var phi_ = Random.Range(0.0f,180.0f);
            var psi_ = Random.Range(0.0f,180.0f);
            var dzi_ = Random.Range(0.0f,180.0f);
            

            ObjInScene.transform.localPosition = new Vector3(x_,y_,z_);

            ObjInScene.transform.eulerAngles = new Vector3(phi_,psi_,dzi_);
            // Debug.Log(ObjInScene.transform.position);

            // Debug.Log(ObjInScene);
            Objs.Add(bbox.object_id, ObjInScene);
            ObjsBoxes.Add(bbox.object_id, bbox);


            last_id_ +=1;
        }

        // Debug.Log("Assets/objects/Cube.prefab");
        // Assets/Resources/Cube.prefab
        // ax bx ay by        
        // float[] box = {0.0f, 10.0f, 0.0f, 10.0f};

        // var prefab = Resources.Load("stool_2") as GameObject;
        // var mesh = prefab.GetComponent<Mesh>();
        // mesh.setM
        // var mesh = Resources.Load("_1") as Mesh;
        // prefab.GetComponent<MeshFilter>().mesh = mesh;
        // Debug.Log(prefab);

        // var ObjInScene = Instantiate(prefab);
        // var bbox = ObjInScene.GetComponent("BBOX") as BBOX;
        // bbox.category = "custom_category_name";
        // bbox.object_id = 1;

        // // Debug.Log(ObjInScene.transform.position);
        // ObjInScene.transform.position = new Vector3(0.0f,-1.3f,0.0f);
        // ObjInScene.transform.eulerAngles = new Vector3(0.0f,0.0f,0.0f);
        // // Debug.Log(ObjInScene.transform.position);

        // var mr = ObjInScene.GetComponent<MeshRenderer>();
        // // mr.material.shader = Shader.Find ("Standard");
        // // mr.material.SetFloat("_Glossiness", 1.0f);
        // mr.material.SetFloat("_GlossMapScale", 1.0f);
        // Objs.Add(bbox.object_id, ObjInScene);
        // ObjsBoxes.Add(bbox.object_id, bbox);
        
    
    }
    // Update is called once per frame
    void Update()
    {
    }

    void ChangeStateOfScene(){
        
        var smoothness_range = new float[]{0.0f,1.0f};
        foreach(var pair in Objs){
            var objid = pair.Key;
            var obj = pair.Value;

            // PLACE object in random position inside box
            var x_ = Random.Range(placement_area[0],placement_area[1]);
            var y_ = Random.Range(placement_area[2],placement_area[3]);
            var z_ = Random.Range(placement_area[4],placement_area[5]);
            var phi_ = Random.Range(0.0f,180.0f);
            var psi_ = Random.Range(0.0f,180.0f);
            var dzi_ = Random.Range(0.0f,180.0f);
            

            obj.transform.localPosition = new Vector3(x_,y_,z_);
            obj.transform.eulerAngles = new Vector3(phi_,psi_,dzi_);

            // Change smoothness of metallic property of material
            var mr = obj.GetComponent<MeshRenderer>();
            mr.material.SetFloat("_GlossMapScale", Random.Range(smoothness_range[0],smoothness_range[1]));
        }


    }
}

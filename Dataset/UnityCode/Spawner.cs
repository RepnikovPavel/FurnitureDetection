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
    
    private GameObject LBulbPrefab;
    private Dictionary<int,GameObject> LightsObjs = new Dictionary<int, GameObject>();
    private Dictionary<int,Light> Lights = new Dictionary<int, Light>();


    float[] placement_area = new float[]{-5.0f, 5.0f, -2.0f,-2.0f, -5.0f, 5.0f};
    float[] light_placement_area = new float[]{-10.0f, 10.0f, 1.0f,5.0f, -10.0f, 10.0f};

    public GameObject wall0;
    public GameObject wall1;
    public GameObject wall2;
    public GameObject wall3;
    public GameObject wall4;
    public GameObject wall5;

    

    // Start is called before the first frame update
    void Start()
    {   


        string[] PrefabsNames = new string[]{
            "stool_1",
            "stool_2"
        };
        string[] PrefabCategory = new string[]{
            "stool",
            "stool"
        };

        // LOAD furniture prefabs
        for(var i=0;i<PrefabsNames.Length;i++){
            var prefab = Resources.Load(PrefabsNames[i]) as GameObject; 
            Prefabs.Add(PrefabsNames[i], prefab);
        }


        // GENERATE objects in scene
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

        // LOAD light prefab
        LBulbPrefab = Resources.Load("LBulb") as GameObject;

        // GENERATE light bulbs
        int num_of_lights_ = 5;
        int light_id_ = 0;
        for(var i =0; i< num_of_lights_;i++){
            var ObjInScene = Instantiate(LBulbPrefab);

            // PLACE object in random position inside box
            var x_ = Random.Range(light_placement_area[0],light_placement_area[1]);
            var y_ = Random.Range(light_placement_area[2],light_placement_area[3]);
            var z_ = Random.Range(light_placement_area[4],light_placement_area[5]);


            ObjInScene.transform.localPosition = new Vector3(x_,y_,z_);

            LightsObjs.Add(light_id_, ObjInScene);
            GameObject child = ObjInScene.transform.GetChild(0).gameObject;
            var light = child.GetComponent<Light>();
            // Debug.Log(light);
            Lights.Add(light_id_,light);
            light.range = 100;

            light_id_ +=1;
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
        if (Input.GetKeyDown("q"))
        {
            // Debug.Log("key pressed");
            ChangeStateOfScene();
        }
    }

    void ChangeStateOfScene(){
        
        var smoothness_range = new float[]{0.0f,1.0f};
        var light_range = new int[]{1,150};
        // UPDATE positions and rotations of furniture
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
        
        // UPDATE ligths positions
        foreach(var pair in LightsObjs){
            var l_id = pair.Key;
            var LightHolder = pair.Value;
            // PLACE object in random position inside box
            var x_ = Random.Range(light_placement_area[0],light_placement_area[1]);
            var y_ = Random.Range(light_placement_area[2],light_placement_area[3]);
            var z_ = Random.Range(light_placement_area[4],light_placement_area[5]);


            LightHolder.transform.localPosition = new Vector3(x_,y_,z_);
        }

        // UPDATE brightness of lights
        foreach(var pair in Lights){
            var light_id_ = pair.Key;
            var light  = pair.Value;
            light.range = (int)Random.Range(light_range[0],light_range[1]);
        }

        // UPDATE smoothness of walls
        wall0.GetComponent<MeshRenderer>().material.SetFloat("_GlossMapScale", Random.Range(smoothness_range[0],smoothness_range[1]));
        wall1.GetComponent<MeshRenderer>().material.SetFloat("_GlossMapScale", Random.Range(smoothness_range[0],smoothness_range[1]));
        wall2.GetComponent<MeshRenderer>().material.SetFloat("_GlossMapScale", Random.Range(smoothness_range[0],smoothness_range[1]));
        wall3.GetComponent<MeshRenderer>().material.SetFloat("_GlossMapScale", Random.Range(smoothness_range[0],smoothness_range[1]));
        wall4.GetComponent<MeshRenderer>().material.SetFloat("_GlossMapScale", Random.Range(smoothness_range[0],smoothness_range[1]));
        wall5.GetComponent<MeshRenderer>().material.SetFloat("_GlossMapScale", Random.Range(smoothness_range[0],smoothness_range[1]));


    }
}

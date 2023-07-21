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


    public float[] placement_area = new float[]{-5.0f, 5.0f, 0.0f,0.0f, -5.0f, 5.0f};
    public float[] light_placement_area = new float[]{-10.0f, 10.0f, 0.0f,5.0f, -10.0f, 10.0f};

    private int last_id_ = 0;
    public int current_index_of_batch_=0;
    public bool IsInitStep = true; 
    public GameObject wall0;
    public GameObject wall1;
    public GameObject wall2;
    public GameObject wall3;
    public GameObject wall4;
    public GameObject wall5;

    public string[] PrefabsNames;
    public Dictionary<int,string> PrefabCategory = new Dictionary<int, string>();
    // public List<KeyValuePair<string,int>> PrefabCategoryIdByName = new List<KeyValuePair<string, int>>();
    public Dictionary<string,int> Categories = new Dictionary<string, int>();

    public bool IsStartEnd = false;
    // Start is called before the first frame update
    void Start()
    {   
        IsStartEnd = true;
    }
    // Update is called once per frame
    void Update()
    {
    }

    public void InitDictWithPrefabs(){
        Categories.Add("stool",0);
        Categories.Add("chair",1);
        Categories.Add("sofa",2);
        Categories.Add("bench",3);
        Categories.Add("bed",4);
        Categories.Add("TV",5);
        Categories.Add("table",6);
        Categories.Add("wardrobe",7);
        Categories.Add("storage",8);
        Categories.Add("refrigerator",9);
        Categories.Add("microwave",10);


        PrefabsNames = new string[]{
            "stool_1",
            "stool_2",
            "chair_1",
            "chair_2",
            "sofa_1",
            "sofa_2",
            "bench_1",
            "bench_2",
            "bed_1",
            "bed_2",
            "TV_1",
            "table_1",
            "table_2",
            "table_3",
            "wardrobe_1",
            "storage_1",
            "storage_2",
            "refrigerator_1",
            "microwave_1"
        }; 
        
        // Debug.Log(PrefabCategory);
        PrefabCategory.Add(0,"stool");
        PrefabCategory.Add(1,"stool");
        PrefabCategory.Add(2,"chair");
        PrefabCategory.Add(3,"chair");
        PrefabCategory.Add(4,"sofa");
        PrefabCategory.Add(5,"sofa");
        PrefabCategory.Add(6,"bench");
        PrefabCategory.Add(7,"bench");
        PrefabCategory.Add(8,"bed");
        PrefabCategory.Add(9,"bed");
        PrefabCategory.Add(10,"TV");
        PrefabCategory.Add(11,"table");
        PrefabCategory.Add(12,"table");
        PrefabCategory.Add(13,"table");
        PrefabCategory.Add(14,"wardrobe");
        PrefabCategory.Add(15,"storage");
        PrefabCategory.Add(16,"storage");
        PrefabCategory.Add(17,"refrigerator");
        PrefabCategory.Add(18,"microwave");
    }
    public void LoadFurniturePrefabs(){
        for(var i=0;i<PrefabsNames.Length;i++){
            // Debug.Log(PrefabsNames[i]);
            var prefab = Resources.Load(PrefabsNames[i]) as GameObject; 
            Prefabs.Add(PrefabsNames[i], prefab);
        }
        // for(var i= 0;i<PrefabsNames.Length;i++){
        //     Debug.Log(PrefabCategory[i]);
        //     PrefabCategoryIdByName.Add(new KeyValuePair<string,int>(PrefabCategory[i],i));
        // }
    }
    public void CreateObjectsInScene(){

        int low_ = 0;
        int high_ = PrefabsNames.Length-1;
        int num_of_objects_ = 3 + (int)Random.Range(0.0f,5.0f);


        // GENERATE object from ith prefab
        // to ensure that all prefabs are included in the data set guaranteed

        if(current_index_of_batch_>=PrefabsNames.Length){
            current_index_of_batch_ =0;
        }

        var forced_prefab_name_ = PrefabsNames[current_index_of_batch_];
        var forsed_obj_ = Instantiate(Prefabs[forced_prefab_name_]);
        var bbox_ = forsed_obj_.GetComponent("BBOX") as BBOX;
        var forced_category = PrefabCategory[current_index_of_batch_];
        bbox_.category = forced_category;
        bbox_.object_id = last_id_;
        var x__ = Random.Range(placement_area[0],placement_area[1]);
        var y__ = Random.Range(placement_area[2],placement_area[3]);
        var z__ = Random.Range(placement_area[4],placement_area[5]);
        // var phi_ = Random.Range(0.0f,180.0f);
        // var psi_ = Random.Range(0.0f,180.0f);
        var phi__ = 0.0f;
        var psi__ = Random.Range(0.0f,180.0f);
        var dzi__ = 0.0f;
        forsed_obj_.transform.position = transform.position + new Vector3(x__,y__,z__);
        forsed_obj_.transform.eulerAngles =new Vector3(phi__,psi__,dzi__);
        Objs.Add(bbox_.object_id, forsed_obj_);
        ObjsBoxes.Add(bbox_.object_id, bbox_);
        last_id_ +=1;

        // GENERATE objs from random prefab
        // x1 x2 y1 y2 z1 z2
        for(var i =1; i< num_of_objects_-1;i++){
            int name_pos_ = Mathf.RoundToInt(Random.Range((float)low_,(float)high_));
            var prefab_name_ = PrefabsNames[name_pos_];
            var ObjInScene = Instantiate(Prefabs[prefab_name_]);
            var bbox = ObjInScene.GetComponent("BBOX") as BBOX;
            // Debug.Log(bbox);
            // SET category name and object in scene id
            // Debug.Log(PrefabCategory[name_pos_]);
            bbox.category = PrefabCategory[name_pos_];
            bbox.object_id = last_id_;

            // PLACE object in random position inside box
            var x_ = Random.Range(placement_area[0],placement_area[1]);
            var y_ = Random.Range(placement_area[2],placement_area[3]);
            var z_ = Random.Range(placement_area[4],placement_area[5]);
            // var phi_ = Random.Range(0.0f,180.0f);
            // var psi_ = Random.Range(0.0f,180.0f);
            var phi_ = 0.0f;
            var psi_ = Random.Range(0.0f,180.0f);
            var dzi_ = 0.0f;
            

            ObjInScene.transform.position = transform.position + new Vector3(x_,y_,z_);
            ObjInScene.transform.eulerAngles =new Vector3(phi_,psi_,dzi_);
            // Debug.Log(ObjInScene.transform.position);

            // Debug.Log(ObjInScene);
            Objs.Add(bbox.object_id, ObjInScene);
            ObjsBoxes.Add(bbox.object_id, bbox);
            last_id_ +=1;
        }
        current_index_of_batch_ +=1;
    }
    public void DeteleObjectsInScene(){
        foreach(var pair in Objs){
            var objid = pair.Key;
            var Obj = pair.Value;
            // var ObjBox =  ObjsBoxes[objid];
            Destroy(Obj);
        }
        foreach(var pair in ObjsBoxes){
            var objid = pair.Key;
            var Obj = pair.Value;
            // var ObjBox =  ObjsBoxes[objid];
            Destroy(Obj);
        }
        Objs.Clear();
        ObjsBoxes.Clear();
    }
    public void CreateLightInScene(){
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


            ObjInScene.transform.position = transform.position+ new Vector3(x_,y_,z_);

            LightsObjs.Add(light_id_, ObjInScene);
            GameObject child = ObjInScene.transform.GetChild(0).gameObject;
            var light = child.GetComponent<Light>();
            // Debug.Log(light);
            Lights.Add(light_id_,light);
            light.range = 100;

            light_id_ +=1;
        }
    }

    public void ChangeStateOfScene(int camera_state, int number_of_camera_states){
        
        if (IsInitStep){
            CreateLightInScene();
            CreateObjectsInScene();
            IsInitStep = false;
        }
        if (camera_state>=number_of_camera_states){
            // need reload new objects to scene
            DeteleObjectsInScene();
            CreateObjectsInScene();
        }

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
            // var phi_ = Random.Range(0.0f,180.0f);
            // var psi_ = Random.Range(0.0f,180.0f);
            // var dzi_ = Random.Range(0.0f,180.0f);
            var phi_ = 0.0f;
            var psi_ = Random.Range(0.0f,180.0f);
            var dzi_ = 0.0f;

            obj.transform.position = transform.position+ new Vector3(x_,y_,z_);
            obj.transform.localEulerAngles = new Vector3(phi_,psi_,dzi_);

            // Change smoothness of metallic property of material
            // var mr = obj.GetComponent<MeshRenderer>();
            // mr.material.SetFloat("_GlossMapScale", Random.Range(smoothness_range[0],smoothness_range[1]));
        }
        
        // UPDATE ligths positions
        foreach(var pair in LightsObjs){
            var l_id = pair.Key;
            var LightHolder = pair.Value;
            // PLACE object in random position inside box
            var x_ = Random.Range(light_placement_area[0],light_placement_area[1]);
            var y_ = Random.Range(light_placement_area[2],light_placement_area[3]);
            var z_ = Random.Range(light_placement_area[4],light_placement_area[5]);


            LightHolder.transform.position = transform.position+ new Vector3(x_,y_,z_);
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

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using UnityEditor;

public class Spawner : MonoBehaviour
{
    Dictionary<string, GameObject> Objs;
    // Start is called before the first frame update
    void Start()
    {   

        // var BaseDir = "/home/user/UnityProjects/MakeDataset/Assets/objects";
        var BaseDir = "objects";
        var ObjsURL = new List<string>();
        ObjsURL.Add(Path.Join(BaseDir,"Cube"));
        Debug.Log("Assets/objects/Cube.prefab");
        // Assets/Resources/Cube.prefab
        // ax bx ay by        
        float[] box = {0.0f, 10.0f, 0.0f, 10.0f};
        int N = 10;

        var prefab = Resources.Load("Cube") as GameObject;
        var ObjInScene = Instantiate(prefab, new Vector3(0.0f,0.0f,0.0f), Quaternion.identity);
        Objs.Add(ObjsURL[0],ObjInScene);
        
    
    }
    // Update is called once per frame
    void Update()
    {
    }
}

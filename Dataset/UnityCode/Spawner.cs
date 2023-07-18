using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class Spawner : MonoBehaviour
{
    Dictionary<string, GameObject> Objs;
    // Start is called before the first frame update
    void Start()
    {   

        var BaseDir = "/home/user/UnityProjects/MakeDataset/Assets/objects";
        var ObjsURL = new List<string>();
        ObjsURL.Add(Path.Join(BaseDir,"Cube"));
        // ax bx ay by        
        float[] box = {0.0f, 10.0f, 0.0f, 10.0f};
        int N = 10;

        
        GameObject prefab = Resources.Load(ObjsURL[0]) as GameObject;
        var ObjInScene = Instantiate(prefab, new Vector3(0.0f,0.0f,0.0f), Quaternion.identity);
        Objs.Add(ObjsURL[0],ObjInScene);
        

    }

    // Update is called once per frame
    void Update()
    {
    }
}

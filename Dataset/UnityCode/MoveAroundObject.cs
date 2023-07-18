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

    Camera camera;
    IEnumerator Start(){
        camera = Camera.main;
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
    }

    // IEnumerator WriteImg(){
        // yield return WriteImg_();
    // }

    IEnumerator WriteImg_(){
        yield return new WaitForEndOfFrame();
        Debug.Log("write img call");
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
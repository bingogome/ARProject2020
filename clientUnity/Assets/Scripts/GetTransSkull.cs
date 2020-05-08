using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GetTransSkull : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        var pos = transform.localPosition;
        var rot = transform.localRotation;
        Debug.Log("Skull transformation rot: " + rot.ToString("0.0000000"));
        Debug.Log("Skull transformation pos: " + pos.ToString("0.0000000"));
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}

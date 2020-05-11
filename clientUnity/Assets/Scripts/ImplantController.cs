using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class ImplantController : MonoBehaviour
{
    
    // Start is called before the first frame update
    //void Start()
    //{
        
    //}

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKey(KeyCode.UpArrow))
        {
            Vector3 current = new Vector3(0,0,0.001f);
            transform.localPosition += current;
        }
        if (Input.GetKey(KeyCode.DownArrow))
        {
            Vector3 current = new Vector3(0, 0, -0.001f);
            transform.localPosition += current;
        }
        if (Input.GetKey(KeyCode.LeftArrow))
        {
            Vector3 current = new Vector3(-0.001f, 0, 0);
            transform.localPosition += current;
        }
        if (Input.GetKey(KeyCode.RightArrow))
        {
            Vector3 current = new Vector3(0.001f, 0, 0);
            transform.localPosition += current;
        }
        if (Input.GetKey(KeyCode.W))
        {
            Vector3 current = new Vector3(0, 0.001f, 0);
            transform.localPosition += current;
        }
        if (Input.GetKey(KeyCode.S))
        {
            Vector3 current = new Vector3(0, -0.001f, 0);
            transform.localPosition += current;
        }
        if (Input.GetKey(KeyCode.Q))
        {
            Vector3 current = new Vector3(0, 0, 0.5f);
            if(this.CompareTag("Mesh"))
                transform.localEulerAngles -= current;
            else
                transform.localEulerAngles += current;
        }
        if (Input.GetKey(KeyCode.E))
        {
            Vector3 current = new Vector3(0, 0, -0.5f);
            if (this.CompareTag("Mesh"))
                transform.localEulerAngles -= current;
            else
                transform.localEulerAngles += current;
        }
        if (Input.GetKey(KeyCode.A))
        {
            Vector3 current = new Vector3(-0.5f, 0, 0);
            transform.localEulerAngles += current;
        }
        if (Input.GetKey(KeyCode.D))
        {
            Vector3 current = new Vector3(0.5f, 0, 0);
            transform.localEulerAngles += current;
        }
        if (Input.GetKey(KeyCode.Z))
        {
            Vector3 current = new Vector3(0, 0.5f, 0);
            transform.localEulerAngles += current;
        }
        if (Input.GetKey(KeyCode.C))
        {
            Vector3 current = new Vector3(0, -0.5f, 0);
            transform.localEulerAngles += current;
        }

    }

}

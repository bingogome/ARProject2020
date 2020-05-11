using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class TextController : MonoBehaviour
{
    private Vector3 pos = new Vector3(0, 0, 0);
    private Quaternion quat = new Quaternion(0, 0, 0, 1);
    public Text PosQuatText;
    // Start is called before the first frame update
    void Start()
    {
        UpdateText();
    }

    // Update is called once per frame
    void Update()
    {
        UpdateText();
    }
    void UpdateText()
    {
        pos = transform.localPosition;
        quat = transform.localRotation;
        PosQuatText.text = "Position: " + pos.ToString("0.00000") + " Quaternion: " + quat.ToString("0.00000");
    }
}

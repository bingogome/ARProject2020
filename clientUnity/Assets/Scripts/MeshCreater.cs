using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(MeshFilter))]
public class MeshCreater : MonoBehaviour
{

    [System.Serializable]
    public class ImplantMesh
    {
        public ImplantMeshJson GetImplantMesh;
    }

    [System.Serializable]
    public class ImplantMeshJson
    {
        public float[] vertices;
        public int[] triangles;
        public float[] color;
    }
    private UDPClient udpClient;

    // Start is called before the first frame update
    void Start()
    {
        udpClient = GetComponent<UDPClient>();

        //Mesh mesh = new Mesh();
        //GetComponent<MeshFilter>().mesh = mesh;
        //Vector3[] verticesTest;
        //int[] trianglesTest;
        //verticesTest = new Vector3[]
        //{
        //        new Vector3 (0,0,0),
        //        new Vector3 (0,0,1),
        //        new Vector3 (1,0,0),
        //        new Vector3 (1,0,1)
        //};
        //trianglesTest = new int[]
        //{
        //        0,1,2,
        //        1,3,2
        //};

        //mesh.Clear();
        //mesh.vertices = verticesTest;
        //mesh.triangles = trianglesTest;


    }

    // Update is called once per frame
    void Update()
    {
        
        string message = "";

        message = udpClient.GetLatestUDPPacket();
        
        ImplantMesh m = JsonUtility.FromJson<ImplantMesh>(message);

        if (message != "")
        {
            Mesh mesh = new Mesh();
            GetComponent<MeshFilter>().mesh = mesh;
            Debug.Log(m.GetImplantMesh.triangles);
            Vector3[] vertices = new Vector3[m.GetImplantMesh.vertices.Length / 3];

            for (int i = 0; i < m.GetImplantMesh.vertices.Length / 3; i++)
                vertices[i] = new Vector3(m.GetImplantMesh.vertices[3 * i], m.GetImplantMesh.vertices[3 * i + 1], m.GetImplantMesh.vertices[3 * i + 2]);

            mesh.Clear();
            mesh.vertices = vertices;
            mesh.triangles = m.GetImplantMesh.triangles;
            Color[] colors = new Color[mesh.vertices.Length];
            for (int i = 0; i < mesh.vertices.Length; i++)
                colors[i] = colors[i] = Color.Lerp(Color.blue, Color.red, m.GetImplantMesh.color[i]);
            mesh.colors = colors;
            mesh.RecalculateNormals();

        }




    }
}

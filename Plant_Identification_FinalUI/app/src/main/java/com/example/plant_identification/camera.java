package com.example.plant_identification;

import androidx.activity.result.ActivityResult;
import androidx.activity.result.ActivityResultCallback;
import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.content.Intent;
import android.graphics.Bitmap;
import android.util.Base64;
import android.widget.ImageView;
import android.widget.Toast;
import android.widget.ImageButton;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.RetryPolicy;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import java.io.ByteArrayOutputStream;
import java.util.HashMap;
import java.util.Map;

public class camera extends AppCompatActivity {
    ImageView imageView; //Image view
    String imageUrl = "https://buddy-boy4.ecn.purdue.edu/~jhuang/uploadImage.php"; //Upload Image URL
    String executeUrl = "https://buddy-boy4.ecn.purdue.edu/~jhuang/executePy.php"; //Execute Python Script URL
    Bitmap bitmap;

    //Redo Camera Launcher - Joseph Huang
    ActivityResultLauncher<Intent> startForResult = registerForActivityResult(new ActivityResultContracts.StartActivityForResult(), new ActivityResultCallback<ActivityResult>() {
        @Override
        public void onActivityResult(ActivityResult result) {
            if (result != null && result.getResultCode() == RESULT_OK) {
                if (result.getData() != null) {
                    Bitmap photo = (Bitmap) result.getData().getExtras().get("data");
                    imageView.setImageBitmap(photo);
                    bitmap = photo;
                }
            }
        }
    });

    //onCreate Method - Joseph Huang
    @Override
    public void onCreate(Bundle savedInstanceState) {
        //Open Camera Activity on Android (9/9/2022)
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_camera);

        //Buttons replaced by photoButtons to work correctly with UI (kwl 11/8/2022)
        imageView = this.findViewById(R.id.disp_img);
        ImageButton photoButton = this.findViewById(R.id.takepicture);
        ImageButton uploadButton = this.findViewById(R.id.upload);
        ImageButton displayResults = this.findViewById(R.id.display);

        //Start Camera (9/10/22)
        photoButton.setOnClickListener(v -> {
            Intent cameraIntent = new Intent(android.provider.MediaStore.ACTION_IMAGE_CAPTURE);
            //startActivityForResult(cameraIntent, 1888); //need to look for alternative for startActivityForResult since it is depreciated
            startForResult.launch(cameraIntent); //new method (replacing startActivityForResult)
        });


        //onClick listener for upload button
        //create hash map containing image in string form
        //pass the string to php file
        uploadButton.setOnClickListener(view ->
        {
            StringRequest stringRequest = new StringRequest(Request.Method.POST, imageUrl, response -> Toast.makeText(getApplicationContext(), response, Toast.LENGTH_LONG).show(), error -> Toast.makeText(getApplicationContext(), "ERROR: " + error.toString(), Toast.LENGTH_LONG).show()) {
                @Override
                protected Map<String, String> getParams() {
                    Map<String, String> params = new HashMap<>();
                    String imageString = imageToString(bitmap);
                    params.put("image", imageString);

                    return params;
                }
            };

            // This function makes the time required for timeout error to be 60 seconds
            // This was the workaround for the issue we had with timeout errors on the actual phone
            stringRequest.setRetryPolicy(new RetryPolicy() {
                @Override
                public int getCurrentTimeout() {
                    return 60000;
                }
                @Override
                public int getCurrentRetryCount() {
                    return 60000;
                }
                @Override
                public void retry(VolleyError error) throws VolleyError {
                }
            });

            RequestQueue requestQueue = Volley.newRequestQueue(camera.this);
            requestQueue.add(stringRequest);
        });

        //redo display results onClick Listener for better readability
        displayResults.setOnClickListener(view -> {
            StringRequest resultRequest = new StringRequest(Request.Method.POST, executeUrl, response -> Toast.makeText(getApplicationContext(), "Plant Type: " + response, Toast.LENGTH_LONG).show(), error -> Toast.makeText(getApplicationContext(), "ERROR: " + error.toString(), Toast.LENGTH_LONG).show());
            RequestQueue requestQueue = Volley.newRequestQueue(camera.this);
            requestQueue.add(resultRequest);
        });
    }
    /* //This has been replaced by ActivityResultLauncher - Joseph Huang
    //Get Image Back From Camera - Joseph Huang
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == 1888) {
            Bitmap photo = (Bitmap) data.getExtras().get("data");
            imageView.setImageBitmap(photo);
            bitmap = photo;
        }
    }*/

    //imageToString - Joseph Huang
    private String imageToString(Bitmap bitmap) {
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
        bitmap.compress(Bitmap.CompressFormat.JPEG, 100, outputStream);
        byte[] imageBytes = outputStream.toByteArray();
        return (Base64.encodeToString(imageBytes, Base64.DEFAULT));
    }

}



using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;
using Bds_project.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;

using System.Text.Json;
using System.Diagnostics;

namespace Bds_project.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class ModelController : ControllerBase
    {
    

        private readonly ILogger<ModelController> _logger;

        public ModelController(ILogger<ModelController> logger)
        {
            _logger = logger;
        }

        [HttpPost("trainModel")]
        public String RowsCols([FromBody] DataFrame df)
        {
            Console.WriteLine(df.data);
            Console.WriteLine(df.columns);

            df.columns.RemoveAt(0);

           // Console.WriteLine(callFunctionPost(df));
            return callFunctionPost(df, "https://bdsfunc.azurewebsites.net/api/Bdsfunc?");
        }

        [HttpPost("testModel")]
        public string RandomForest([FromBody] DataFrame df)
        {
            df.columns.RemoveAt(0);
            return callFunctionPost(df, "https://bdsfunc.azurewebsites.net/api/httptrigger2?");
        }


        public String callFunctionPost(DataFrame df, string url)
        {
  
            var request = WebRequest.Create(url);
            request.Method = "POST";

            var json = JsonSerializer.Serialize(df);
            byte[] byteArray = Encoding.UTF8.GetBytes(json);
            Console.WriteLine(json.Substring(0,500));
            Console.WriteLine(json.Length);
            Console.WriteLine(json.Substring(json.Length-500));

            request.ContentType = "application/x-www-form-urlencoded";
            request.ContentLength = byteArray.Length;

            using var reqStream = request.GetRequestStream();
            reqStream.Write(byteArray, 0, byteArray.Length);

            using var response = request.GetResponse();

            using var respStream = response.GetResponseStream();

            using var reader = new StreamReader(respStream);
            string data = reader.ReadToEnd();
            Console.WriteLine(response);
            Console.WriteLine(data);
            //JObject rss = JObject.Parse(data);

            //Stats stats1 = rss.ToObject<Stats>();

            return data;
        }
    }
}

using System;
using System.Collections.Generic;
using Newtonsoft.Json;

namespace Bds_project.Models
{
    public class DataFrame
    {
        [JsonProperty("data")]
        public List<Data> data { get; set; }
        [JsonProperty("columns")]
        public List<string> columns { get; set; }

        [JsonProperty("container_name")]
        public string container_name { get; set; }

        public DataFrame(List<Data> data, List<string> columns,string container_name)
        {
            this.data = data;
            this.columns = columns;
            this.container_name = container_name;
        }
        public DataFrame()
        {

        }
    }
}

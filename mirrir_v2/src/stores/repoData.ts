import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import type { List } from 'echarts'

const m_rooturl='http://10.181.232.2:8000'

interface LanguageDetail{
  value:  number;
  name: string;
}

interface BasicData{
  stars: number;
  pulls: number;
  issues: number;
  open_pulls: number;
  language: string;
  language_detail: Array<LanguageDetail>
  forks: number;
  description: string;
  contributor: number;
  close_pulls: number;
}

interface Data{
  basicData: BasicData
}

export const repoDataStore = defineStore('repoData',{
  state: () =>({
    val: []
  }),
  actions: {
    async addData(userName: String,repoName: String) {
      let tmp_data={};

      try{
        // basic data
        await axios
        .get(m_rooturl + "/get_basic",{
          params: {
            repo: repoName,
            user: userName
          }
        })
        .then(response => {
          tmp_data.basicData = JSON.parse(response.data)
          turn_into_percentage(tmp_data.basicData.language_detail)
        })

        // commit activity
        await axios
        .get(m_rooturl + "/get_commit_activity",{
          params: {
            repo: repoName
          }
        })
        .then(response => {
          tmp_data.commitActivity = JSON.parse(response.data).result
        })

        // company data
        await axios
        .get(m_rooturl + '/get_issue_creator', {
          params: {
            repo: 'pytorch'
          },
        })
        .then(response => {
          tmp_data.bubbledata = JSON.parse(response.data).result
        })

        // user data
        await axios
        .get(m_rooturl + '/get_user' , {
          params: {
            owner: 'pytorch',
            repo: 'pytorch'
          }
        })
        .then(response => {
          tmp_data.userData = JSON.parse(response.data).result
        })
        
        console.log(tmp_data)
        this.val.push(tmp_data)
        // let cpy = JSON.parse(JSON.stringify(tmp_data));
        // this.val.push(cpy)
      } catch (err){
        console.log(err)
      }
    }
  },
})

// deal with language_detail
function turn_into_percentage( language_detail ){
  console.log(language_detail)
  // sum all
  let all_line = 0;
  for(let i=0;i<language_detail.length;i++){
    all_line+= language_detail[i].value;
  }

  // divide all
  for(let i=0;i<language_detail.length;i++){
    language_detail[i].value /=  all_line;
  }

  console.log(language_detail)
}